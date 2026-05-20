import random
import pandas as pd
from collections import Counter

# Curated skill benchmarks for standard modern technical roles
ROLE_BENCHMARKS = {
    "Frontend Developer": {
        "required": ["javascript", "typescript", "react", "html", "css", "tailwind", "bootstrap", "git"],
        "advanced": ["angular", "vue", "node.js", "next.js", "graphql", "sass", "postman"],
        "roadmap": [
            "**Phase 1: Foundations & Core Technologies (Weeks 1-4)**: Deeply master JavaScript (ES6+ features like promises, async/await, DOM manipulation), clean HTML5 semantic structures, and responsive layouts using modern CSS3.",
            "**Phase 2: Modern Frameworks & State Management (Weeks 5-8)**: Pick up React or Angular. Build a robust understanding of component life cycles, props/state, hooks, and global state management tools (like Redux or Context API).",
            "**Phase 3: Utility Styling, Tooling & APIs (Weeks 9-12)**: Adopt utility-first frameworks like Tailwind CSS. Practice writing highly modular, reusable components and learn to test web requests and APIs using Postman or Swagger."
        ],
        "projects": [
            "**Interactive Analytics Dashboard**: Construct a modern React dashboard featuring glassmorphic designs, responsive sidebar navigation, and live data charts (e.g., using Plotly or Chart.js) integrated with public REST APIs.",
            "**Collaborative Workspace Platform**: Develop a drag-and-drop Kanban style task-board using TypeScript and Vue or React, utilizing local storage or a mock backend for persistence."
        ]
    },
    "Backend Developer": {
        "required": ["python", "java", "node.js", "sql", "mysql", "postgresql", "mongodb", "git"],
        "advanced": ["go", "rust", "django", "flask", "fastapi", "spring", "express", "redis", "docker", "gcp", "aws"],
        "roadmap": [
            "**Phase 1: Language Mastery & Database Design (Weeks 1-4)**: Solidify your knowledge in a primary backend language (Python, Java, or Node.js) and master relational database schemas, normalization, and complex SQL joins using PostgreSQL or MySQL.",
            "**Phase 2: Frameworks, APIs & Authentication (Weeks 5-8)**: Deepen knowledge in a professional web framework (FastAPI, Django, Spring Boot, or Express). Build scalable RESTful endpoints, implement JWT/OAuth2 authentication, and use custom middleware.",
            "**Phase 3: Caching, Containerization & Infrastructure (Weeks 9-12)**: Implement database caching with Redis, write clean unit tests, containerize applications with Docker, and learn database indexing techniques for query optimization."
        ],
        "projects": [
            "**RESTful E-Commerce Engine**: Implement a secure backend with FastAPI and PostgreSQL. Include features like product catalogs, JWT-based user session control, a shopping cart logic, and simulated stripe payments.",
            "**Microservices Real-Time Messenger**: Build a real-time communications backend with Node.js/Express and WebSockets, utilizing Redis for pub/sub mechanisms and Docker to manage container images."
        ]
    },
    "Full-Stack Developer": {
        "required": ["javascript", "react", "node.js", "express", "sql", "postgresql", "mongodb", "git", "docker"],
        "advanced": ["typescript", "angular", "vue", "next.js", "graphql", "aws", "gcp", "redis", "kubernetes"],
        "roadmap": [
            "**Phase 1: Full-Stack Basics & API Integration (Weeks 1-4)**: Master React for the frontend and Node.js with Express for the backend. Build simple CRUD applications connecting both ends using Git for source control.",
            "**Phase 2: Database Layer & TypeScript (Weeks 5-8)**: Bridge the stack with both relational (PostgreSQL) and non-relational (MongoDB) databases. Introduce TypeScript across both client and server to catch type-level bugs early.",
            "**Phase 3: Production Deployment & Scale (Weeks 9-12)**: Learn to containerize your stack with Docker, utilize Redis to cache session states, and deploy your frontend and backend on modern cloud platforms (like AWS EC2/S3 or Heroku)."
        ],
        "projects": [
            "**Corporate SaaS Platform**: Create a complete software-as-a-service web portal (e.g. subscription manager) with React, Node.js, Express, and MongoDB. Secure it using custom middleware, and integrate billing simulation.",
            "**Social Discovery Application**: Build a real-time web portal featuring map integration, image storage, feed search, and interactive feedback using Next.js, Express, PostgreSQL, and AWS S3."
        ]
    },
    "Data Scientist / AI Engineer": {
        "required": ["python", "r", "sql", "pandas", "numpy", "scikit-learn", "matplotlib", "git"],
        "advanced": ["tensorflow", "pytorch", "keras", "tableau", "power bi", "fastapi", "aws", "gcp", "docker"],
        "roadmap": [
            "**Phase 1: Mathematical Foundations & Data Wrangling (Weeks 1-4)**: Master Python programming alongside numerical analysis packages (Pandas, NumPy). Deepen your math intuition in linear algebra, statistics, and probability.",
            "**Phase 2: Classical Machine Learning (Weeks 5-8)**: Study supervised and unsupervised ML models (Linear/Logistic Regression, Decision Trees, Random Forests, K-Means) using Scikit-Learn. Learn cross-validation and feature engineering.",
            "**Phase 3: Deep Learning & MLOps Pipelines (Weeks 9-12)**: Transition to deep learning with PyTorch or TensorFlow for neural networks. Learn to package your model as a production API using FastAPI and containerize it using Docker."
        ],
        "projects": [
            "**End-to-End Model Deployer**: Train an optimal regression or classification model (e.g., house valuation or customer churn prediction) using Scikit-Learn, build a REST API using FastAPI, and present it with a beautiful interactive Streamlit dashboard.",
            "**Computer Vision Classifier**: Implement a custom Convolutional Neural Network (CNN) in PyTorch or TensorFlow to classify images, integrating automated preprocessing and data augmentation pipelines."
        ]
    },
    "DevOps & Cloud Engineer": {
        "required": ["linux", "bash", "git", "docker", "aws", "terraform", "jenkins"],
        "advanced": ["kubernetes", "gcp", "azure", "ansible", "chef", "puppet", "circleci", "travisci", "datadog", "splunk"],
        "roadmap": [
            "**Phase 1: Shell scripting & Linux Administration (Weeks 1-4)**: Build complete comfort with Linux operating systems, file permissions, shell environments, advanced Bash scripting, and Git branching workflows.",
            "**Phase 2: CI/CD & Containerization (Weeks 5-8)**: Containerize complex application stacks using multi-stage Dockerfiles. Set up automated continuous integration (CI) pipelines using GitHub Actions or Jenkins.",
            "**Phase 3: Infrastructure as Code & Orchestration (Weeks 9-12)**: Learn to script and deploy cloud architectures (AWS) declaratively using Terraform (IaC). Transition to Kubernetes (EKS/GKE) for automated application container orchestration."
        ],
        "projects": [
            "**Declarative AWS Infrastructure**: Create and deploy a highly secure, multi-tier AWS VPC configuration complete with private/public subnets, security groups, RDS instances, and an S3 bucket entirely provisioned using Terraform.",
            "**GitOps Kubernetes Pipeline**: Set up a continuous delivery flow where pushing source code builds a Docker image, tests it, pushes it to Docker Hub, and automatically triggers an update on a local or remote Kubernetes cluster."
        ]
    },
    "Data Engineer": {
        "required": ["python", "scala", "sql", "postgresql", "mysql", "git", "aws", "gcp"],
        "advanced": ["spark", "hadoop", "mongodb", "cassandra", "elasticsearch", "redis", "terraform", "docker"],
        "roadmap": [
            "**Phase 1: Relational Modeling & Complex Querying (Weeks 1-4)**: Acquire expert-level SQL skills. Master indexing, database triggers, optimization of queries, and schema designs (e.g., star and snowflake schemas).",
            "**Phase 2: Distributed Computing & ETL Pipelines (Weeks 5-8)**: Learn distributed computing architectures. Master Apache Spark or PySpark for processing large datasets in memory. Create automated extract-transform-load (ETL) routines.",
            "**Phase 3: Big Data Ecosystems & Warehousing (Weeks 9-12)**: Integrate NoSQL systems (MongoDB, Cassandra) for unstructured data. Understand modern Cloud Data Warehouses (like Amazon Redshift or Snowflake) and orchestrate pipelines using Apache Airflow."
        ],
        "projects": [
            "**Clickstream Streaming Processor**: Deploy a real-time data streaming environment. Collect mock web clicks via Apache Kafka, process streams dynamically in PySpark, and output structured aggregates into PostgreSQL.",
            "**Cloud-Native Data Warehouse ETL**: Script an automated ETL workflow on AWS using Lambda functions and Glue triggers to capture raw CSV data uploaded to S3, clean/transform it, and write it to Amazon Redshift."
        ]
    },
    "Software Engineer (General)": {
        "required": ["python", "java", "c++", "c#", "git", "sql", "linux"],
        "advanced": ["docker", "kubernetes", "aws", "typescript", "node.js", "postgresql", "mongodb", "redis"],
        "roadmap": [
            "**Phase 1: Programming Mastery & Data Structures (Weeks 1-4)**: Achieve deep fluency in a core programming language (Python, Java, or C++). Practice solving algorithmic challenges focusing on time/space complexities (Big O).",
            "**Phase 2: OOP & Architectural Patterns (Weeks 5-8)**: Study Object-Oriented Design (OOD), SOLID design patterns, and MVC system structures. Learn how to interface applications cleanly with databases using SQL.",
            "**Phase 3: System Design & Enterprise Tooling (Weeks 9-12)**: Introduce microservice architectures, caching layers, and deployment utilities. Learn Docker, Linux server management, and basic AWS cloud hosting concepts."
        ],
        "projects": [
            "**High-Performance Key-Value Store**: Write a custom, thread-safe, distributed in-memory key-value database in Go or Java supporting basic network communication and data replication features.",
            "**Microservices Task Platform**: Build a system made of multiple backend microservices (e.g., auth, task creation, reporting) communicating over REST or gRPC, backed by individual databases and containerized with Docker."
        ]
    }
}

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

def generate_detailed_recommendations(selected_role, role_type, all_skills, df=None, analysis=None):
    """
    Generates highly detailed and comprehensive recommendations based on selected role and current skills.
    Returns:
        A dict with:
        - 'role_name': Name of selected role
        - 'matching_percentage': float percentage of matching skills
        - 'found_skills': list of matched skills
        - 'missing_required': list of missing required skills
        - 'missing_advanced': list of missing advanced skills
        - 'roadmap': list of step-by-step roadmap items
        - 'projects': list of project suggestions
    """
    all_skills_lower = [s.lower() for s in all_skills]
    
    if role_type == "Predefined Tech Roles (Recommended)":
        benchmark = ROLE_BENCHMARKS.get(selected_role, ROLE_BENCHMARKS["Software Engineer (General)"])
        req_skills = benchmark["required"]
        adv_skills = benchmark["advanced"]
        roadmap = benchmark["roadmap"]
        projects = benchmark["projects"]
        
        found_req = [s for s in req_skills if s.lower() in all_skills_lower]
        missing_req = [s for s in req_skills if s.lower() not in all_skills_lower]
        
        found_adv = [s for s in adv_skills if s.lower() in all_skills_lower]
        missing_adv = [s for s in adv_skills if s.lower() not in all_skills_lower]
        
        # Calculate fit match based on required skills
        total_req_skills = len(req_skills)
        match_pct = round((len(found_req) / total_req_skills) * 100) if total_req_skills > 0 else 0
        
        return {
            "role_name": selected_role,
            "matching_percentage": match_pct,
            "found_skills": found_req + found_adv,
            "missing_required": missing_req,
            "missing_advanced": missing_adv,
            "roadmap": roadmap,
            "projects": projects
        }
    else:
        # Dynamic search from dataset category
        if df is not None:
            df_cat = df[df["Category"] == selected_role]
        else:
            df_cat = pd.DataFrame()
            
        if len(df_cat) > 0:
            # Collect all skills for this category to find dominant ones
            cat_skills = []
            for _, row in df_cat.iterrows():
                cat_skills.extend([s.lower() for s in row.get('Extracted_Programming_Languages', [])])
                cat_skills.extend([s.lower() for s in row.get('Extracted_Frameworks', [])])
                cat_skills.extend([s.lower() for s in row.get('Extracted_Tools', [])])
                cat_skills.extend([s.lower() for s in row.get('Extracted_Databases', [])])
                cat_skills.extend([s.lower() for s in row.get('Extracted_Cloud', [])])
                
            skill_counts = Counter(cat_skills)
            # Take top 8 skills as required and next 6 as advanced
            top_common = [skill for skill, count in skill_counts.most_common(20)]
            req_skills = top_common[:8] if len(top_common) >= 8 else top_common
            adv_skills = top_common[8:14] if len(top_common) > 8 else []
        else:
            req_skills = ["python", "sql", "git"]
            adv_skills = ["docker", "aws"]
            
        # If no skills are extracted for a non-tech category (like ARTS or CHEF), ensure some basic placeholder
        if not req_skills:
            req_skills = ["word", "excel", "communication"]
            adv_skills = ["leadership", "management"]
            
        found_req = [s for s in req_skills if s.lower() in all_skills_lower]
        missing_req = [s for s in req_skills if s.lower() not in all_skills_lower]
        
        found_adv = [s for s in adv_skills if s.lower() in all_skills_lower]
        missing_adv = [s for s in adv_skills if s.lower() not in all_skills_lower]
        
        total_req_skills = len(req_skills)
        match_pct = round((len(found_req) / total_req_skills) * 100) if total_req_skills > 0 else 0
        
        # Build dynamic, tailored roadmap
        roadmap = [
            f"**Phase 1: Foundational Category Standards (Weeks 1-4)**: Focus on mastering core expectations in this category, notably {', '.join(req_skills[:3]).title()}.",
            f"**Phase 2: Operational Tools & Frameworks (Weeks 5-8)**: Familiarize yourself with key supportive utilities like {', '.join(req_skills[3:6]).title()} to streamline your workflow.",
            f"**Phase 3: Specialized & Advanced Capabilities (Weeks 9-12)**: Stand out by developing expertise in premium/advanced assets: {', '.join(adv_skills[:3]).title() if adv_skills else 'Advanced domain knowledge'}."
        ]
        
        # Build dynamic project suggestions
        projects = [
            f"**Domain Process Automation**: Design a comprehensive workflow implementation that integrates {', '.join(req_skills[:3]).title()} to showcase optimization of business or technical routines.",
            f"**Advanced Analytics & Case Study**: Build a structured analysis model, portfolio, or case study incorporating {', '.join(adv_skills[:2]).title() if adv_skills else 'domain best practices'} to demonstrate deep problem-solving skills."
        ]
        
        return {
            "role_name": f"{selected_role} (Dataset Profile)",
            "matching_percentage": match_pct,
            "found_skills": found_req + found_adv,
            "missing_required": missing_req,
            "missing_advanced": missing_adv,
            "roadmap": roadmap,
            "projects": projects
        }
