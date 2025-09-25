from pymongo import MongoClient
import pandas as pd
from config import MONGO_URI, MONGO_DB_NAME

class MongoHandler:
    """Handles interactions with MongoDB for YouTube data."""
    def __init__(self):
        self.client = MongoClient(MONGO_URI)
        self.db = self.client[MONGO_DB_NAME]
        self.collection = self.db['youtube_comments']

    def insert_data(self, df):
        if not df.empty:
            records = df.to_dict('records')
            for record in records:
                # Use comment_id as the unique identifier
                self.collection.update_one({'comment_id': record['comment_id']}, {'$set': record}, upsert=True)
            print(f"Inserted/Updated {len(records)} YouTube comments.")

    def find_data_by_keyword(self, keyword):
        cursor = self.collection.find({'keyword': keyword})
        df = pd.DataFrame(list(cursor))
        if '_id' in df.columns:
            df.drop('_id', axis=1, inplace=True)
        return df