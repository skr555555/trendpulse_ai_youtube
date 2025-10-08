import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Import project modules
from src.data_collection.collector import YouTubeCollector
from src.database.db_handler import MongoHandler
from src.processing.preprocessor import clean_text
from src.analysis.sentiment import get_sentiment
from src.analysis.trends import get_trends_over_time, get_top_videos
from src.analysis.influencers import get_top_channels

st.set_page_config(page_title="TrendPulse AI - YouTube", layout="wide", page_icon="📺")

@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_and_process_data(keyword, video_limit, comment_limit):
    db_handler = MongoHandler()
    df = db_handler.find_data_by_keyword(keyword)
    
    # Simple check to see if we need to fetch more data
    if len(df) < (video_limit * comment_limit * 0.5): # Heuristic to refetch if data is sparse
        st.info("Fetching new data from YouTube API...")
        collector = YouTubeCollector()
        new_df = collector.fetch_video_data_by_keyword(keyword, video_limit, comment_limit)
        if not new_df.empty:
            db_handler.insert_data(new_df)
            df = db_handler.find_data_by_keyword(keyword)
    
    if df.empty: return None

    df['cleaned_text'] = df['comment_text'].apply(clean_text)
    df['sentiment'] = df['cleaned_text'].apply(get_sentiment)
    return df

st.title("📺 TrendPulse AI: YouTube Analytics Dashboard")
st.markdown("Enter a keyword to analyze recent video comments, top channels, and trends.")

with st.sidebar:
    st.header("⚙️ Controls")
    keyword_input = st.text_input("Enter a search keyword", value="AI in 2025")
    video_limit = st.slider("Number of videos to scan", 5, 50, 10)
    comment_limit = st.slider("Comments per video to analyze", 10, 100, 20)
    analyze_button = st.button("Analyze Trends", type="primary")

if analyze_button and keyword_input:
    with st.spinner(f"Analyzing '{keyword_input}'... This might take a moment."):
        df = load_and_process_data(keyword_input, video_limit, comment_limit)

    if df is not None and not df.empty:
        st.success(f"Analysis complete! Found {len(df)} comments for '{keyword_input}'.")
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "🏆 Top Content", "📺 Top Channels", "📝 Raw Data"])
        
        with tab1:
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Comment Sentiment Distribution")
                sentiment_counts = df['sentiment'].value_counts()
                fig = px.pie(sentiment_counts, values=sentiment_counts.values, names=sentiment_counts.index, title="Comment Sentiment")
                st.plotly_chart(fig, use_container_width=True)
            with col2:
                st.subheader("Most Frequent Words in Comments")
                text = " ".join(df['cleaned_text'])
                wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
                fig, ax = plt.subplots(); ax.imshow(wordcloud, interpolation='bilinear'); ax.axis('off')
                st.pyplot(fig)

        with tab2:
            st.subheader("Comment Activity Over Time")
            trends_df = get_trends_over_time(df)
            fig = px.line(trends_df, x='comment_published_at', y='count', title='Comment Volume per Day')
            st.plotly_chart(fig, use_container_width=True)

            st.subheader("Most Viewed Videos in Sample")
            top_videos_df = get_top_videos(df)
            st.dataframe(top_videos_df)
            
        with tab3:
            st.subheader("Top Performing Channels")
            st.markdown("Channels are ranked based on a score derived from the views, likes, and comments on the videos found in the sample.")
            influencers_df = get_top_channels(df)
            st.dataframe(influencers_df, use_container_width=True)
        
        with tab4:
            st.subheader("Raw Comment Data")
            st.dataframe(df[['comment_published_at', 'comment_text', 'sentiment', 'video_title', 'channel_title', 'like_count', 'view_count']])
    else:
        st.error(f"No data found for '{keyword_input}'. This could be due to API limits or no results. Please try another keyword.")
else:
    st.info("Enter a keyword in the sidebar to begin.")