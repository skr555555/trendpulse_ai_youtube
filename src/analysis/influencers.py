import pandas as pd

def get_top_channels(df, top_n=10):
    """
    Identifies top channels based on engagement metrics.
    """
    if df.empty or 'channel_title' not in df.columns:
        return pd.DataFrame()

    # Group by channel and aggregate metrics
    channel_stats = df.groupby('channel_title').agg(
        total_views=('view_count', 'mean'),  # Use mean as videos are repeated
        total_likes=('like_count', 'mean'),
        comments_in_sample=('comment_id', 'count')
    ).reset_index()

    # Create a simple engagement score
    channel_stats['engagement_score'] = (
        channel_stats['total_views'] * 0.5 +
        channel_stats['total_likes'] * 0.3 +
        channel_stats['comments_in_sample'] * 0.2
    )

    # Sort and return the top N channels
    top_channels = channel_stats.sort_values(by='engagement_score', ascending=False).head(top_n)
    
    # Format for better display
    top_channels['total_views'] = top_channels['total_views'].astype(int)
    top_channels['total_likes'] = top_channels['total_likes'].astype(int)

    return top_channels[['channel_title', 'total_views', 'total_likes', 'comments_in_sample', 'engagement_score']]