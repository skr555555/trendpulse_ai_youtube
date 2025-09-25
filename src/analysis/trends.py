import pandas as pd
from collections import Counter

def get_trends_over_time(df, time_col='comment_published_at', time_unit='D'):
    """Analyzes comment frequency over time."""
    if df.empty: return pd.DataFrame()
    df[time_col] = pd.to_datetime(df[time_col])
    trends = df.set_index(time_col).resample(time_unit).size().reset_index(name='count')
    return trends

def get_top_videos(df, top_n=10):
    """Gets the most commented-on or viewed videos in the sample."""
    if df.empty: return pd.DataFrame()
    top_vids = df.groupby('video_title')['view_count'].mean().sort_values(ascending=False).head(top_n)
    return top_vids.reset_index()