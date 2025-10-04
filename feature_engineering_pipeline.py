import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from src.database.db_handler import MongoHandler
from src.analysis.sentiment import get_sentiment
from src.processing.preprocessor import clean_text_multilingual

# --- Configuration ---
NUM_TOPICS = 5 # The number of topics you want to discover
NUM_TOP_WORDS = 10 # Words per topic

class FeatureEngineer:
    def __init__(self):
        self.db_handler = MongoHandler()
        self.raw_collection = self.db_handler.db['youtube_comments']
        self.featured_collection = self.db_handler.db['youtube_comments_featured']

    def compute_engagement_metrics(self, doc):
        """Computes a normalized engagement ratio."""
        views = doc.get('view_count', 0)
        likes = doc.get('like_count', 0)
        if views > 0:
            doc['engagement_ratio'] = (likes / views) * 100
        else:
            doc['engagement_ratio'] = 0
        return doc

    def run_topic_modeling(self, documents):
        """Trains an LDA model on all English comments and assigns topics."""
        english_docs = [doc for doc in documents if doc.get('language') == 'en']
        if not english_docs:
            print("No English documents found for topic modeling.")
            return documents

        # Use CountVectorizer for LDA
        vectorizer = CountVectorizer(max_df=0.9, min_df=2, stop_words='english')
        X = vectorizer.fit_transform([doc['cleaned_text'] for doc in english_docs])
        
        # Train LDA model
        lda = LatentDirichletAllocation(n_components=NUM_TOPICS, random_state=42)
        lda.fit(X)

        # Assign topics to each English document
        topic_distributions = lda.transform(X)
        for i, doc in enumerate(english_docs):
            doc['topic_distribution'] = topic_distributions[i].tolist()
            doc['dominant_topic'] = int(topic_distributions[i].argmax())
        
        return documents

    def create_indexes(self):
        """Creates indexes on the new collection to speed up queries."""
        print("Creating database indexes...")
        self.featured_collection.create_index("keyword")
        self.featured_collection.create_index("channel_title")
        self.featured_collection.create_index("dominant_topic")
        print("Indexes created successfully.")

    def run(self):
        """Main function to run the entire feature engineering pipeline."""
        print("Starting feature engineering pipeline...")
        # 1. EXTRACT: Load all data from the raw collection
        all_documents = list(self.raw_collection.find())
        if not all_documents:
            print("No documents found in the raw collection. Exiting.")
            return

        # 2. TRANSFORM: Apply feature engineering steps
        print(f"Processing {len(all_documents)} documents...")
        
        # Compute engagement and sentiment for all docs
        featured_docs = [self.compute_engagement_metrics(doc) for doc in all_documents]
        
        # Run Topic Modeling on the entire dataset
        featured_docs = self.run_topic_modeling(featured_docs)

        # 3. LOAD: Save to the new feature-rich collection
        print(f"Saving {len(featured_docs)} feature-rich documents to the new collection...")
        # Clear the old collection before inserting new data to avoid duplicates
        self.featured_collection.delete_many({})
        self.featured_collection.insert_many(featured_docs)
        
        # 4. OPTIMIZE: Create indexes
        self.create_indexes()

        print("Feature engineering pipeline completed successfully!")

if __name__ == "__main__":
    engineer = FeatureEngineer()
    engineer.run()