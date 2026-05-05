import pandas as pd
import joblib
import os
from preprocessing import preprocess_dataframe
from extraction import apply_extraction
from embeddings import generate_tfidf_embeddings
from clustering import apply_kmeans, reduce_dimensions, add_clustering_results_to_df
from analysis import analyze_clusters, identify_strong_weak_clusters, detect_skill_gaps

def run_pipeline(data_path, output_dir='output'):
    print("Starting pipeline...")
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Load Data
    print(f"Loading data from {data_path}...")
    try:
        df = pd.read_csv(data_path)
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return
        
    # Sample data if it's too large for quick processing during dev
    if len(df) > 1000:
        print("Dataset is large, sampling 1000 records for efficient processing...")
        df = df.sample(1000, random_state=42).reset_index(drop=True)
        
    # 2. Preprocessing
    df = preprocess_dataframe(df)
    
    # 3. Extraction
    df = apply_extraction(df)
    
    # 4. Embeddings
    X_tfidf, vectorizer = generate_tfidf_embeddings(df)
    joblib.dump(vectorizer, os.path.join(output_dir, 'tfidf_vectorizer.pkl'))
    
    # 5. Clustering
    clusters, kmeans_model = apply_kmeans(X_tfidf, n_clusters=4)
    joblib.dump(kmeans_model, os.path.join(output_dir, 'kmeans_model.pkl'))
    
    # Dimensionality Reduction for visualization
    reduced_embeddings = reduce_dimensions(X_tfidf, method='pca')
    df = add_clustering_results_to_df(df, clusters, reduced_embeddings)
    
    # 6. Analysis
    cluster_analysis = analyze_clusters(df)
    strong_id, weak_id = identify_strong_weak_clusters(cluster_analysis)
    
    print(f"Strongest Cluster: {strong_id}")
    print(f"Weakest Cluster: {weak_id}")
    
    # 7. Skill Gap
    skill_gaps = detect_skill_gaps(cluster_analysis, strong_id, weak_id)
    print(f"Detected Skill Gaps for Weakest Cluster: {skill_gaps}")
    
    # Save processed dataframe
    output_data_path = os.path.join(output_dir, 'processed_resumes.pkl')
    df.to_pickle(output_data_path)
    print(f"Processed data saved to {output_data_path}")
    
    # Save analysis results
    joblib.dump({
        'cluster_analysis': cluster_analysis,
        'strongest_cluster': strong_id,
        'weakest_cluster': weak_id,
        'skill_gaps': skill_gaps
    }, os.path.join(output_dir, 'analysis_results.pkl'))
    print("Analysis results saved.")
    print("Pipeline completed successfully!")

if __name__ == "__main__":
    DATA_PATH = "datasets/Resume/Resume.csv"
    run_pipeline(DATA_PATH)
