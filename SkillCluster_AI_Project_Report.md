# Project Report: SkillCluster AI

## 1. Introduction
**SkillCluster AI** is an end-to-end Machine Learning and Natural Language Processing (NLP) project designed to automate the analysis of student resumes. The primary objective is to group similar resumes, identify hidden skill gaps, and recommend personalized learning paths to improve candidates' placement readiness.

## 2. Problem Statement
In the competitive job market, students often struggle to understand what specific skills they are missing compared to top-tier candidates. Placement cells and recruiters also face challenges in manually analyzing hundreds of resumes to group candidates by skill sets. There is a need for an automated, AI-driven platform that can evaluate resumes, cluster them intelligently, and provide actionable insights.

## 3. Dataset
The project utilizes the **Resume Dataset** (sourced from Kaggle), containing a diverse set of resumes across various job categories. 
- **Core Column**: `Resume_str` (The raw textual content of the resumes).
- **Target Variable**: None (This is an Unsupervised Learning task).

## 4. Methodology
The pipeline consists of the following key stages:

### 4.1 Data Preprocessing
Raw resume text undergoes rigorous cleaning to prepare it for machine learning algorithms:
- Lowercasing and punctuation removal.
- URLs, emails, and special character filtering using Regular Expressions (Regex).
- Tokenization and Stopword Removal using `NLTK`.
- Lemmatization to reduce words to their base form.

### 4.2 NLP Information Extraction
A custom rule-based extraction engine maps cleaned text against an extensive technology dictionary to extract:
- Programming Languages (Python, Java, C++, etc.)
- Frameworks (React, Django, Flask, etc.)
- Tools (Git, Docker, Kubernetes, etc.)
- Databases and Cloud Platforms (AWS, Azure, MySQL, etc.)

### 4.3 Feature Engineering (Embeddings)
The cleaned resume text is converted into a numerical vector space using **TF-IDF (Term Frequency-Inverse Document Frequency) Vectorization**. This approach accurately represents the importance of specific technical keywords relative to the entire resume corpus.

### 4.4 Unsupervised Clustering
**K-Means Clustering** (with k=4) is applied to the TF-IDF embeddings to group resumes into distinct clusters based on semantic similarity and skill overlap. **Principal Component Analysis (PCA)** is utilized to reduce the dimensionality of the embeddings into a 2D space for interactive visualization.

### 4.5 Skill Gap Analysis & Recommendation
The system analyzes the generated clusters to calculate the average skill density per cluster. 
- The cluster with the highest average skills is designated as the **Strongest Cluster**.
- The cluster with the lowest average skills is designated as the **Weakest Cluster**.
- By performing a comparative analysis of the top frequencies, the algorithm detects critical **Skill Gaps** (technologies present in the strong cluster but missing in the weak cluster).
- A **Recommendation Engine** generates personalized learning paths based on these missing skills to help weaker candidates upskill.

## 5. Streamlit Dashboard
The results are presented through a highly interactive, modern web application built with **Streamlit**. 
Key features of the dashboard include:
- **Glassmorphism UI**: Premium visual aesthetics with animated backgrounds.
- **Dataset Overview**: High-level metrics regarding data distributions and job categories.
- **Cluster Insights**: 2D scatter projections of the candidate groupings and dominant technologies per cluster.
- **Skill Gap Detection**: Heatmaps comparing skill distributions between top-tier and lower-tier groups.
- **Resume Analyzer**: A live text-input tool that allows users to paste a resume, instantly classify it into a cluster, and receive a tailored AI learning path.

## 6. Tech Stack
- **Languages:** Python
- **Data Manipulation:** Pandas, NumPy
- **Machine Learning:** Scikit-learn (K-Means, PCA, TF-IDF)
- **Natural Language Processing:** NLTK, Regular Expressions (re)
- **Visualization:** Plotly (Interactive Charts)
- **Web Framework:** Streamlit, Streamlit-Option-Menu
- **Model Serialization:** Joblib

## 7. Conclusion
SkillCluster AI successfully bridges the gap between raw resume data and actionable placement intelligence. By leveraging NLP and Unsupervised Learning, it eliminates the manual overhead of candidate evaluation, grouping students logically by their technical profiles, and providing data-driven recommendations to maximize their career potential.
