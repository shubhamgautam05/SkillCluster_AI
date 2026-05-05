import pandas as pd
from collections import Counter

def analyze_clusters(df):
    """Generates cluster-level insights."""
    print("Analyzing clusters...")
    
    cluster_analysis = {}
    clusters = df['Cluster'].unique()
    
    for c in clusters:
        cluster_data = df[df['Cluster'] == c]
        
        # Calculate average skill count
        avg_skills = cluster_data['Total_Skills_Count'].mean()
        
        # Collect all skills for this cluster to find dominant ones
        all_skills = []
        for _, row in cluster_data.iterrows():
            all_skills.extend(row['Extracted_Programming_Languages'])
            all_skills.extend(row['Extracted_Frameworks'])
            all_skills.extend(row['Extracted_Tools'])
            all_skills.extend(row['Extracted_Databases'])
            all_skills.extend(row['Extracted_Cloud'])
            
        skill_counts = Counter(all_skills)
        top_skills = [skill for skill, count in skill_counts.most_common(10)]
        
        cluster_analysis[c] = {
            'size': len(cluster_data),
            'avg_skill_count': avg_skills,
            'top_skills': top_skills,
            'skill_frequencies': skill_counts
        }
        
    return cluster_analysis

def identify_strong_weak_clusters(cluster_analysis):
    """Identifies the strongest and weakest clusters based on avg_skill_count."""
    sorted_clusters = sorted(cluster_analysis.items(), key=lambda item: item[1]['avg_skill_count'], reverse=True)
    
    if not sorted_clusters:
        return None, None
        
    strongest_cluster_id = sorted_clusters[0][0]
    weakest_cluster_id = sorted_clusters[-1][0]
    
    return strongest_cluster_id, weakest_cluster_id

def detect_skill_gaps(cluster_analysis, strong_id, weak_id):
    """Detects missing high-value skills in the weak cluster compared to the strong cluster."""
    if strong_id is None or weak_id is None:
        return []
        
    strong_skills = set([skill for skill, count in cluster_analysis[strong_id]['skill_frequencies'].most_common(20)])
    weak_skills = set([skill for skill, count in cluster_analysis[weak_id]['skill_frequencies'].most_common(20)])
    
    # Skills present in strong but missing or rare in weak
    skill_gaps = list(strong_skills - weak_skills)
    
    return skill_gaps
