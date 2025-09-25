import pandas as pd
from googleapiclient.discovery import build
from config import YOUTUBE_API_KEY

class YouTubeCollector:
    """Collects video and comment data from YouTube."""
    def __init__(self):
        if not YOUTUBE_API_KEY:
            raise ValueError("YouTube API Key is not configured in config.py")
        self.youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

    def fetch_video_data_by_keyword(self, keyword, video_limit=10, comment_limit=20):
        """
        Fetches videos for a keyword, then fetches their comments and stats.
        """
        try:
            # 1. Search for videos by keyword
            video_search_request = self.youtube.search().list(
                q=keyword,
                part='snippet',
                type='video',
                order='relevance',
                maxResults=video_limit
            )
            video_response = video_search_request.execute()
            video_ids = [item['id']['videoId'] for item in video_response.get('items', [])]
            if not video_ids: return pd.DataFrame()

            # 2. Get video statistics (views, likes)
            video_stats_request = self.youtube.videos().list(
                part="snippet,statistics",
                id=",".join(video_ids)
            )
            stats_response = video_stats_request.execute()
            video_stats = {item['id']: item for item in stats_response.get('items', [])}

            all_comments_data = []

            # 3. For each video, get its comments
            for video_id in video_ids:
                try:
                    comment_request = self.youtube.commentThreads().list(
                        part='snippet',
                        videoId=video_id,
                        textFormat='plainText',
                        maxResults=comment_limit,
                        order='relevance'
                    )
                    comment_response = comment_request.execute()

                    stats = video_stats.get(video_id, {})
                    snippet = stats.get('snippet', {})
                    statistics = stats.get('statistics', {})

                    for item in comment_response.get('items', []):
                        comment = item['snippet']['topLevelComment']['snippet']
                        all_comments_data.append({
                            'keyword': keyword,
                            'comment_id': item['id'],
                            'comment_text': comment['textDisplay'],
                            'comment_author': comment['authorDisplayName'],
                            'comment_published_at': comment['publishedAt'],
                            'video_id': video_id,
                            'video_title': snippet.get('title', ''),
                            'channel_title': snippet.get('channelTitle', ''),
                            'view_count': int(statistics.get('viewCount', 0)),
                            'like_count': int(statistics.get('likeCount', 0)),
                            'video_comment_count': int(statistics.get('commentCount', 0)),
                        })
                except Exception as e:
                    # Often happens if comments are disabled for a video
                    print(f"Could not fetch comments for video {video_id}: {e}")
                    continue

            return pd.DataFrame(all_comments_data)

        except Exception as e:
            print(f"An error occurred: {e}")
            return pd.DataFrame()