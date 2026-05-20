from sklearn.cluster import KMeans, DBSCAN
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import pandas as pd
import numpy as np

def apply_kmeans(embeddings, n_clusters=4, random_state=42):
    """Applies K-Means clustering to embeddings."""
    print(f"Applying K-Means clustering with k={n_clusters}...")
    kmeans = KMeans(n_clusters=n_clusters, random_state=random_state, n_init=10)
    clusters = kmeans.fit_predict(embeddings)
    return clusters, kmeans

def apply_dbscan(embeddings, eps=0.5, min_samples=5):
    """Applies DBSCAN clustering to embeddings."""
    print(f"Applying DBSCAN clustering with eps={eps}, min_samples={min_samples}...")
    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    clusters = dbscan.fit_predict(embeddings)
    return clusters, dbscan

def reduce_dimensions(embeddings, method='pca', n_components=2, random_state=42):
    """Reduces embeddings to 2D for visualization."""
    print(f"Reducing dimensions using {method.upper()}...")
    if method.lower() == 'pca':
        reducer = PCA(n_components=n_components, random_state=random_state)
    elif method.lower() == 'tsne':
        # Perplexity must be less than n_samples
        perplexity = min(30, max(5, embeddings.shape[0] - 1))
        reducer = TSNE(n_components=n_components, random_state=random_state, perplexity=perplexity)
    else:
        raise ValueError("Method must be 'pca' or 'tsne'")
        
    reduced_embeddings = reducer.fit_transform(embeddings)
    return reduced_embeddings

def add_clustering_results_to_df(df, clusters, reduced_embeddings):
    """Adds cluster labels and 2D coordinates to dataframe."""
    df_out = df.copy()
    df_out['Cluster'] = clusters
    df_out['Dim_1'] = reduced_embeddings[:, 0]
    df_out['Dim_2'] = reduced_embeddings[:, 1]
    return df_out
