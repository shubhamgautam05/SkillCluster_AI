from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

def generate_tfidf_embeddings(df, text_column='Cleaned_Resume', max_features=1000):
    """Generates TF-IDF embeddings from text."""
    print("Generating TF-IDF embeddings...")
    vectorizer = TfidfVectorizer(max_features=max_features)
    X_tfidf = vectorizer.fit_transform(df[text_column]).toarray()
    return X_tfidf, vectorizer

# Removed sentence_transformers to avoid PyTorch Windows DLL issues.
# TF-IDF is used as the baseline for embeddings.
