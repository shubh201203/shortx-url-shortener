"""
Dummy script to generate a pre-trained ML model for URL spam detection.
"""
import os
import joblib
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

def create_dummy_model():
    # Simple dataset
    urls = [
        "https://google.com", "https://github.com", "http://my-safe-site.org",
        "http://free-iphone-winner.spam", "http://cheap-meds-online.xxx",
        "http://crypto-giveaway-fake.com"
    ]
    labels = [0, 0, 0, 1, 1, 1] # 0 = safe, 1 = suspicious

    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(analyzer='char', ngram_range=(2, 4))),
        ('clf', MultinomialNB())
    ])

    pipeline.fit(urls, labels)
    
    # Save the model
    save_path = os.path.join(os.path.dirname(__file__), "spam_model.pkl")
    joblib.dump(pipeline, save_path)
    print(f"Model saved to {save_path}")

if __name__ == "__main__":
    create_dummy_model()
