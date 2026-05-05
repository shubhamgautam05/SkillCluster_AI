import random

def generate_learning_recommendations(missing_skills, extracted_skills_dict=None):
    """
    Generates learning path recommendations based on missing skills.
    extracted_skills_dict is the dict of currently known skills for a specific user to personalize further.
    """
    recommendations = []
    
    if not missing_skills:
        recommendations.append("Your resume shows a strong skill profile. Keep practicing and building advanced projects.")
        return recommendations
        
    # Group missing skills to make targeted recommendations
    missing_langs = [s for s in missing_skills if s in ['python', 'java', 'c++', 'sql', 'javascript']]
    missing_tools = [s for s in missing_skills if s in ['git', 'docker', 'kubernetes', 'jenkins']]
    missing_cloud = [s for s in missing_skills if s in ['aws', 'azure', 'gcp']]
    
    if missing_langs:
        recommendations.append(f"Learn fundamental programming languages/databases: {', '.join(missing_langs).title()}. "
                               f"Focus on practical applications and basic syntax.")
        
    if missing_tools:
        recommendations.append(f"Add essential dev tools to your workflow: {', '.join(missing_tools).title()}. "
                               f"Consider using them in your next project.")
        
    if missing_cloud:
        recommendations.append(f"Cloud skills are highly valued. Consider a beginner certification in: {', '.join(missing_cloud).upper()}.")
        
    if len(missing_skills) > 3:
        recommendations.append("Build 2-3 portfolio projects incorporating these new technologies to demonstrate practical experience.")
    else:
        recommendations.append("Update your resume to explicitly mention these skills once you learn them, using industry-standard keywords.")
        
    return recommendations

def recommend_for_user(user_row, cluster_analysis, strongest_cluster_id):
    """Generates personalized recommendation for a specific row/user."""
    user_cluster = user_row['Cluster']
    user_skills = set(user_row['Extracted_Programming_Languages'] + 
                      user_row['Extracted_Frameworks'] + 
                      user_row['Extracted_Tools'] + 
                      user_row['Extracted_Databases'] + 
                      user_row['Extracted_Cloud'])
                      
    if user_cluster == strongest_cluster_id:
        return ["You belong to a strong cluster! Focus on mastering advanced topics, contributing to open source, or pursuing complex certifications."]
    
    # Compare with strongest cluster top skills
    strong_skills = set([skill for skill, count in cluster_analysis[strongest_cluster_id]['skill_frequencies'].most_common(20)])
    missing_skills = list(strong_skills - user_skills)
    
    return generate_learning_recommendations(missing_skills)
