import re
import pandas as pd

# Predefined dictionaries for extraction
SKILL_DICTIONARY = {
    'programming_languages': ['python', 'java', 'c++', 'c', 'c#', 'javascript', 'typescript', 'ruby', 'php', 'swift', 'go', 'rust', 'kotlin', 'r', 'sql', 'matlab', 'scala', 'dart'],
    'frameworks': ['react', 'angular', 'vue', 'django', 'flask', 'spring', 'express', 'node.js', 'tensorflow', 'keras', 'pytorch', 'scikit-learn', 'pandas', 'numpy', 'bootstrap', 'tailwind', 'hibernate', 'ruby on rails', 'fastapi'],
    'tools': ['git', 'github', 'gitlab', 'bitbucket', 'docker', 'kubernetes', 'jenkins', 'jira', 'confluence', 'trello', 'postman', 'swagger', 'linux', 'bash', 'excel', 'power bi', 'tableau'],
    'databases': ['mysql', 'postgresql', 'mongodb', 'sqlite', 'oracle', 'sql server', 'redis', 'cassandra', 'elasticsearch', 'dynamodb', 'neo4j'],
    'cloud_dev_tools': ['aws', 'azure', 'gcp', 'google cloud', 'heroku', 'terraform', 'ansible', 'chef', 'puppet', 'circleci', 'travisci', 'datadog', 'splunk']
}

def extract_skills_from_text(text):
    """Extracts predefined skills from clean text based on dictionary matching."""
    extracted = {
        'programming_languages': [],
        'frameworks': [],
        'tools': [],
        'databases': [],
        'cloud_dev_tools': []
    }
    
    if not isinstance(text, str):
        return extracted
        
    text_words = set(text.split())
    
    for category, skills in SKILL_DICTIONARY.items():
        for skill in skills:
            # Handle multi-word skills like 'ruby on rails' or 'scikit-learn'
            if ' ' in skill or '-' in skill:
                if skill in text:
                    extracted[category].append(skill)
            else:
                if skill in text_words:
                    extracted[category].append(skill)
                    
    return extracted

def extract_education_keywords(text):
    """Extract education related keywords."""
    education_keywords = ['bachelor', 'master', 'phd', 'degree', 'b.tech', 'm.tech', 'b.sc', 'm.sc', 'b.e', 'm.e', 'diploma', 'university', 'college', 'institute']
    found = []
    text_words = set(text.split())
    for kw in education_keywords:
        if kw in text_words:
            found.append(kw)
    return found

def extract_project_keywords(text):
    """Extract project related keywords."""
    project_keywords = ['project', 'developed', 'designed', 'built', 'created', 'implemented', 'integrated']
    found = []
    text_words = set(text.split())
    for kw in project_keywords:
        if kw in text_words:
            found.append(kw)
    return found

def apply_extraction(df, text_column='Cleaned_Resume'):
    """Applies extraction functions to dataframe and returns structured skills."""
    print("Extracting skills and information...")
    
    skills_series = df[text_column].apply(extract_skills_from_text)
    
    df['Extracted_Programming_Languages'] = skills_series.apply(lambda x: x['programming_languages'])
    df['Extracted_Frameworks'] = skills_series.apply(lambda x: x['frameworks'])
    df['Extracted_Tools'] = skills_series.apply(lambda x: x['tools'])
    df['Extracted_Databases'] = skills_series.apply(lambda x: x['databases'])
    df['Extracted_Cloud'] = skills_series.apply(lambda x: x['cloud_dev_tools'])
    
    df['Education_Keywords'] = df[text_column].apply(extract_education_keywords)
    df['Project_Keywords'] = df[text_column].apply(extract_project_keywords)
    
    # Calculate a simple "Total Skills" count
    df['Total_Skills_Count'] = df.apply(lambda row: len(row['Extracted_Programming_Languages']) + 
                                                   len(row['Extracted_Frameworks']) + 
                                                   len(row['Extracted_Tools']) + 
                                                   len(row['Extracted_Databases']) + 
                                                   len(row['Extracted_Cloud']), axis=1)
    
    return df
