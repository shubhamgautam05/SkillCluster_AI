# 🚀 SkillCluster AI

[![GitHub Repo](https://img.shields.io/badge/GitHub-shubhamgautam05%2FSkillCluster__AI-blue?logo=github)](https://github.com/shubhamgautam05/SkillCluster_AI)
[![Python](https://img.shields.io/badge/Python-3.8%2B-green?logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit)](https://streamlit.io/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Machine_Learning-F7931E?logo=scikit-learn)](https://scikit-learn.org/)

An AI-powered platform using NLP and K-Means clustering to automate resume analysis. It groups candidates by technical proficiency, detects critical industry skill gaps, and generates personalized learning paths. Features a modern Streamlit dashboard to help students visualize their skills and improve their placement readiness.

## ✨ Key Features
- **NLP Information Extraction**: Automatically extracts programming languages, frameworks, and cloud tools from raw, unstructured resume text using `NLTK` and `Regex`.
- **TF-IDF Embeddings**: Converts resume text into dense numerical feature vectors to mathematically represent candidates' technical profiles.
- **Unsupervised Learning**: Implements K-Means clustering to intelligently segment candidates into distinct proficiency groups without needing prior labels.
- **Skill Gap Detection Engine**: Analyzes the top-performing cluster and compares it against weaker clusters to identify missing high-value industry skills (e.g., Git, Docker, AWS).
- **Personalized Recommendations**: Suggests targeted learning paths to students to bridge the detected skill gaps.
- **NextGen Dashboard**: A sleek, glassmorphic UI built with Streamlit and Plotly for highly interactive data visualization and live resume analysis.
- **Full DevOps Pipeline**: Containerized environment with Docker and Docker Compose, robust Makefile for common tasks, and automated GitHub Actions CI/CD pipeline.

---

## 📁 Project Structure

```text
SkillCluster_AI/
│
├── .github/workflows/        # CI/CD pipelines
├── project/                  # Main application directory
│   ├── Dockerfile            # Multi-stage Docker build
│   ├── docker-compose.yml    # Docker Compose setup
│   ├── Makefile              # Helper commands for local dev
│   ├── datasets/             # Ensure your Kaggle Resume.csv is placed here
│   ├── output/               # Auto-generated ML models and clustered data
│   │
│   ├── preprocessing.py      # Cleans text (lowercasing, stopword removal, lemmatization)
│   ├── extraction.py         # NLP rule-based skill extraction engine
│   ├── embeddings.py         # Generates TF-IDF embeddings
│   ├── clustering.py         # K-Means clustering and PCA dimensionality reduction
│   ├── analysis.py           # Evaluates cluster insights and detects skill gaps
│   ├── recommendation.py     # Logic for personalized learning path generation
│   │
│   ├── pipeline.py           # Main pipeline to process data and train the system
│   ├── app.py                # Streamlit frontend dashboard
│   │
│   └── requirements.txt      # Python dependencies
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/shubhamgautam05/SkillCluster_AI.git
cd SkillCluster_AI/project
```

### 2. Run with Docker (Recommended)
The easiest way to run the project is using Docker Compose. If you have `make` installed, you can use the Makefile commands, but standard Docker commands work natively on all platforms (including Windows):

```bash
# Build and start the containers
docker compose up --build
# Or if you have make: make run

# Once running, open a new terminal and execute the ML pipeline inside the container
docker compose --profile pipeline run --rm pipeline-runner
# Or if you have make: make pipeline

# The dashboard will be available at http://localhost:8501
```

To stop the application, simply run:
```bash
docker compose down
# Or if you have make: make stop
```

### 3. Manual Installation (Without Docker)

**Install Dependencies:**
Make sure you have Python installed. Install the required libraries using `pip`:
```bash
pip install -r requirements.txt
```

**Run the ML Pipeline:**
Before starting the app, you need to run the pipeline to generate ML artifacts.
```bash
python pipeline.py
```

**Launch the Dashboard:**
Once the pipeline is complete, launch the Streamlit web application:
```bash
streamlit run app.py
```
> **Note:** The app will automatically open in your default web browser at `http://localhost:8501`.

---

## 📊 Dataset
This project utilizes the **Resume Dataset** (sourced from Kaggle). 
The pipeline specifically targets the `Resume_str` column to perform deep NLP analysis. Make sure the dataset is placed inside `datasets/Resume/Resume.csv`.

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/shubhamgautam05/SkillCluster_AI/issues) if you want to contribute.

## 👨‍💻 Author
**Shubham Gautam**
- GitHub: [@shubhamgautam05](https://github.com/shubhamgautam05)
