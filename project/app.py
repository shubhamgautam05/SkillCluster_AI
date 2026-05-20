import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
from preprocessing import clean_text
from extraction import extract_skills_from_text
from recommendation import generate_learning_recommendations, generate_detailed_recommendations, ROLE_BENCHMARKS

# Set page config
st.set_page_config(page_title="AI Resume Intelligence", page_icon="🚀", layout="wide", initial_sidebar_state="collapsed")

# --- Custom Modern CSS ---
st.markdown("""
<style>
    /* Global Fonts & Colors */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Inter:wght@300;400;600&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
    }
    h1, h2, h3, h4 {
        font-family: 'Outfit', sans-serif;
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #00E5FF, #7B2CBF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Background Animation */
    .stApp {
        background: radial-gradient(circle at top left, rgba(123, 44, 191, 0.15), transparent 40%),
                    radial-gradient(circle at bottom right, rgba(0, 229, 255, 0.1), transparent 40%);
        background-color: #0A0E17;
        background-attachment: fixed;
    }
    
    /* Glassmorphism Metric Cards */
    .glass-card {
        background: rgba(20, 28, 45, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 24px;
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        text-align: center;
        margin-bottom: 20px;
    }
    .glass-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 40px 0 rgba(0, 229, 255, 0.15);
        border: 1px solid rgba(0, 229, 255, 0.2);
    }
    .metric-value {
        font-family: 'Outfit', sans-serif;
        font-size: 3rem;
        font-weight: 800;
        color: #FFFFFF;
        margin: 10px 0;
        text-shadow: 0 0 20px rgba(0, 229, 255, 0.4);
    }
    .metric-label {
        font-size: 1.1rem;
        color: #A0AEC0;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }
    
    /* Tags */
    .skill-tag {
        display: inline-block;
        padding: 6px 14px;
        margin: 4px;
        border-radius: 20px;
        background: linear-gradient(135deg, rgba(0,229,255,0.1), rgba(0,229,255,0.05));
        border: 1px solid rgba(0,229,255,0.2);
        color: #00E5FF;
        font-size: 0.85em;
        font-weight: 600;
        transition: all 0.2s;
    }
    .skill-tag:hover {
        background: rgba(0,229,255,0.2);
        transform: scale(1.05);
    }
    .gap-tag {
        display: inline-block;
        padding: 6px 14px;
        margin: 4px;
        border-radius: 20px;
        background: linear-gradient(135deg, rgba(229,57,53,0.15), rgba(229,57,53,0.05));
        border: 1px solid rgba(229,57,53,0.3);
        color: #FF5252;
        font-size: 0.85em;
        font-weight: 600;
    }
    
    /* Lists */
    .rec-item {
        background: rgba(255,255,255,0.03);
        padding: 15px 20px;
        border-radius: 12px;
        margin-bottom: 10px;
        border-left: 4px solid #7B2CBF;
        transition: background 0.3s;
    }
    .rec-item:hover {
        background: rgba(255,255,255,0.06);
    }
    
    /* Button Animation */
    .stButton>button {
        background: linear-gradient(90deg, #00E5FF 0%, #00B4D8 100%);
        color: #0A0E17 !important;
        font-weight: 700;
        border: none;
        border-radius: 8px;
        padding: 10px 24px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 229, 255, 0.3);
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 6px 20px rgba(0, 229, 255, 0.5);
    }
</style>
""", unsafe_allow_html=True)

# --- Data Loading ---
@st.cache_data
def load_data():
    try:
        df = pd.read_pickle("output/processed_resumes.pkl")
        analysis = joblib.load("output/analysis_results.pkl")
        vectorizer = joblib.load("output/tfidf_vectorizer.pkl")
        kmeans_model = joblib.load("output/kmeans_model.pkl")
        return df, analysis, vectorizer, kmeans_model
    except Exception as e:
        return None, None, None, None

df, analysis, vectorizer, kmeans_model = load_data()

if df is None:
    st.error("Model artifacts not found! Please run the pipeline script.")
    st.stop()

# --- Top Navigation ---
st.markdown("<div style='text-align: center; margin-bottom: 30px;'><h1>🚀 SkillCluster AI</h1><p style='color: #A0AEC0; font-size: 1.2rem;'>AI-Powered Placement Readiness & Skill Gap Detection</p></div>", unsafe_allow_html=True)

selected = option_menu(
    menu_title=None,
    options=["Dashboard", "Cluster Insights", "Skill Gaps", "Resume Analyzer"],
    icons=["house", "bar-chart-fill", "shield-exclamation", "robot"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "rgba(20,28,45,0.6)", "border-radius": "15px", "border": "1px solid rgba(255,255,255,0.05)"},
        "icon": {"color": "#00E5FF", "font-size": "18px"},
        "nav-link": {"font-size": "16px", "text-align": "center", "margin": "0px", "font-weight": "600", "font-family": "Inter"},
        "nav-link-selected": {"background-color": "rgba(0, 229, 255, 0.1)", "color": "#00E5FF", "border-radius": "15px"},
    }
)

st.markdown("<br>", unsafe_allow_html=True)

# --- 1. Dashboard ---
if selected == "Dashboard":
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="glass-card">
            <div class="metric-label">Total Resumes</div>
            <div class="metric-value">{len(df)}</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        cat_count = df['Category'].nunique() if 'Category' in df.columns else 'N/A'
        st.markdown(f"""
        <div class="glass-card">
            <div class="metric-label">Job Categories</div>
            <div class="metric-value">{cat_count}</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="glass-card">
            <div class="metric-label">Clusters Formed</div>
            <div class="metric-value">{df['Cluster'].nunique()}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><h3>Data Distribution</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Category Pie Chart
        if 'Category' in df.columns:
            cat_counts = df['Category'].value_counts().reset_index()
            cat_counts.columns = ['Category', 'Count']
            fig_pie = px.pie(cat_counts, names='Category', values='Count', hole=0.4, 
                             color_discrete_sequence=px.colors.sequential.Plasma)
            fig_pie.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", 
                                  font=dict(color="white"), showlegend=False, title="Categories")
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_pie, use_container_width=True)
            
    with col2:
        # Cluster Bar Chart
        cluster_counts = df['Cluster'].value_counts().reset_index()
        cluster_counts.columns = ['Cluster', 'Count']
        cluster_counts['Cluster'] = cluster_counts['Cluster'].astype(str)
        fig_bar = px.bar(cluster_counts, x='Cluster', y='Count', color='Cluster',
                         color_discrete_sequence=["#7B2CBF", "#00E5FF", "#48CAE4", "#9D4EDD"],
                         title="Resumes per Cluster")
        fig_bar.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="white"))
        st.plotly_chart(fig_bar, use_container_width=True)

# --- 2. Cluster Insights ---
elif selected == "Cluster Insights":
    st.markdown("<h3>AI Cluster Projection</h3>", unsafe_allow_html=True)
    
    fig_scatter = px.scatter(
        df, x='Dim_1', y='Dim_2', color=df['Cluster'].astype(str),
        hover_data=['Category', 'Total_Skills_Count'] if 'Category' in df.columns else ['Total_Skills_Count'],
        color_discrete_sequence=["#00E5FF", "#7B2CBF", "#F72585", "#4CC9F0"],
        opacity=0.8
    )
    fig_scatter.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", 
        plot_bgcolor="rgba(0,0,0,0)", 
        font=dict(color="white"),
        height=500,
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(showgrid=False, zeroline=False, visible=False),
        yaxis=dict(showgrid=False, zeroline=False, visible=False)
    )
    fig_scatter.update_traces(marker=dict(size=8, line=dict(width=1, color='rgba(255,255,255,0.5)')))
    st.plotly_chart(fig_scatter, use_container_width=True)
    
    st.markdown("<br><h3>Cluster Skill Profiles</h3>", unsafe_allow_html=True)
    
    clusters = sorted(df['Cluster'].unique())
    tabs = st.tabs([f"Cluster {c}" for c in clusters])
    
    for i, tab in enumerate(tabs):
        with tab:
            st.markdown("<br>", unsafe_allow_html=True)
            top_skills = analysis['cluster_analysis'][i]['top_skills']
            avg_skills = round(analysis['cluster_analysis'][i]['avg_skill_count'], 1)
            
            col_a, col_b = st.columns([1, 2])
            with col_a:
                st.markdown(f"""
                <div class="glass-card" style="padding: 15px;">
                    <div class="metric-label">Avg. Skills Detected</div>
                    <div class="metric-value" style="font-size: 2rem;">{avg_skills}</div>
                </div>
                """, unsafe_allow_html=True)
                
            with col_b:
                st.markdown("<b>Dominant Technologies:</b><br>", unsafe_allow_html=True)
                skills_html = "".join([f"<span class='skill-tag'>{s.upper()}</span>" for s in top_skills])
                st.markdown(skills_html, unsafe_allow_html=True)

# --- 3. Skill Gaps ---
elif selected == "Skill Gaps":
    strong_id = analysis['strongest_cluster']
    weak_id = analysis['weakest_cluster']
    skill_gaps = analysis['skill_gaps']
    
    st.markdown("<h3>Comparative Analysis</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="glass-card" style="border-top: 4px solid #00E5FF;">
            <h4 style="margin:0;">🏆 Strongest Group (Cluster {strong_id})</h4>
            <p style="color: #A0AEC0; margin-top: 10px;">High skill density, rich tech stack.</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="glass-card" style="border-top: 4px solid #FF5252;">
            <h4 style="margin:0;">⚠️ Weakest Group (Cluster {weak_id})</h4>
            <p style="color: #A0AEC0; margin-top: 10px;">Missing industry-standard tools.</p>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br><h3>🚨 Critical Skill Gaps</h3>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:#A0AEC0;'>Technologies present in the strongest cluster but missing in the weakest:</p>", unsafe_allow_html=True)
    
    if skill_gaps:
        gaps_html = "".join([f"<span class='gap-tag'>{s.upper()}</span>" for s in skill_gaps])
        st.markdown(f"<div style='margin-bottom: 30px;'>{gaps_html}</div>", unsafe_allow_html=True)
    else:
        st.success("No significant skill gaps detected!")
        
    st.markdown("<h3>Skill Heatmap</h3>", unsafe_allow_html=True)
    
    strong_freqs = analysis['cluster_analysis'][strong_id]['skill_frequencies']
    weak_freqs = analysis['cluster_analysis'][weak_id]['skill_frequencies']
    all_top_skills = set([s for s, c in strong_freqs.most_common(12)] + [s for s, c in weak_freqs.most_common(12)])
    
    heatmap_data = []
    for skill in all_top_skills:
        heatmap_data.append({
            'Skill': skill.upper(),
            f'Cluster {strong_id}': strong_freqs.get(skill, 0),
            f'Cluster {weak_id}': weak_freqs.get(skill, 0)
        })
        
    df_heat = pd.DataFrame(heatmap_data).set_index('Skill')
    fig_heat = px.imshow(df_heat.T, color_continuous_scale='Purpor', aspect="auto")
    fig_heat.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="white"))
    st.plotly_chart(fig_heat, use_container_width=True)

# --- 4. Resume Analyzer ---
elif selected == "Resume Analyzer":
    st.markdown("<h3>🎯 Intelligent Resume Analyzer</h3>", unsafe_allow_html=True)
    
    st.markdown("<p style='color: #A0AEC0;'>Select a targeted role benchmark below to ensure hyper-focused skill-gap analysis and precise learning roadmaps.</p>", unsafe_allow_html=True)
    
    col_bench_1, col_bench_2 = st.columns(2)
    with col_bench_1:
        benchmark_type = st.radio(
            "Select Benchmark Reference Type:",
            ["Predefined Tech Roles (Recommended)", "Dataset Categories"],
            horizontal=True
        )
    with col_bench_2:
        if benchmark_type == "Predefined Tech Roles (Recommended)":
            selected_role = st.selectbox(
                "Choose Targeted Tech Role:",
                list(ROLE_BENCHMARKS.keys())
            )
        else:
            db_categories = sorted(df['Category'].unique()) if df is not None else []
            selected_role = st.selectbox(
                "Choose Dataset Category:",
                db_categories
            )
            
    resume_text = st.text_area("Paste candidate resume text here for live analysis...", height=200)
    
    if st.button("🚀 Analyze Candidate Profile"):
        if not resume_text:
            st.error("Please provide resume text to analyze.")
        else:
            with st.spinner("Running deep NLP analysis and custom recommendation mapping..."):
                cleaned = clean_text(resume_text)
                extracted_skills = extract_skills_from_text(cleaned)
                all_skills = extracted_skills['programming_languages'] + extracted_skills['frameworks'] + extracted_skills['tools'] + extracted_skills['databases'] + extracted_skills['cloud_dev_tools']
                
                tfidf_vec = vectorizer.transform([cleaned]).toarray()
                cluster_pred = kmeans_model.predict(tfidf_vec)[0]
                
                # Use the new detailed recommendation generator
                detailed_recs = generate_detailed_recommendations(
                    selected_role=selected_role,
                    role_type=benchmark_type,
                    all_skills=all_skills,
                    df=df,
                    analysis=analysis
                )

            st.markdown("<br>", unsafe_allow_html=True)
            col1, col2 = st.columns([1.1, 1.4])
            
            with col1:
                st.markdown("<div class='glass-card' style='text-align: left; margin-bottom: 20px;'>", unsafe_allow_html=True)
                st.markdown("<h4>🧠 Profile Overview</h4>", unsafe_allow_html=True)
                st.markdown(f"<p style='color: #A0AEC0;'>Assigned Dataset Cluster: <b style='color: white;'>Cluster {cluster_pred}</b></p>", unsafe_allow_html=True)
                
                st.markdown("<hr style='border-color: rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
                st.markdown("<b>Detected Languages & Databases:</b><br>", unsafe_allow_html=True)
                combined = extracted_skills['programming_languages'] + extracted_skills['databases']
                if combined:
                    st.markdown("".join([f"<span class='skill-tag'>{s}</span>" for s in combined]), unsafe_allow_html=True)
                else:
                    st.markdown("<span style='color:gray;'>None detected</span>", unsafe_allow_html=True)
                    
                st.markdown("<br><b>Detected Frameworks & Tools:</b><br>", unsafe_allow_html=True)
                combined2 = extracted_skills['frameworks'] + extracted_skills['tools'] + extracted_skills['cloud_dev_tools']
                if combined2:
                    st.markdown("".join([f"<span class='skill-tag'>{s}</span>" for s in combined2]), unsafe_allow_html=True)
                else:
                    st.markdown("<span style='color:gray;'>None detected</span>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Fit Score Card
                st.markdown(f"""
                <div class="glass-card" style="border-top: 4px solid #00E5FF; text-align: center;">
                    <div class="metric-label">Job Fit Match Score</div>
                    <div class="metric-value">{detailed_recs['matching_percentage']}%</div>
                    <p style="color: #A0AEC0; font-size: 0.95rem; margin-top: 5px;">Target: <b>{detailed_recs['role_name']}</b></p>
                </div>
                """, unsafe_allow_html=True)
                
                # Benchmark Skill Details Card
                st.markdown("<div class='glass-card' style='text-align: left;'>", unsafe_allow_html=True)
                st.markdown("<h4>🎯 Benchmark Breakdown</h4>", unsafe_allow_html=True)
                
                # Found
                st.markdown("<b style='color: #2ECC71;'>Matched Benchmark Skills:</b><br>", unsafe_allow_html=True)
                if detailed_recs['found_skills']:
                    found_html = "".join([f"<span class='skill-tag' style='background: rgba(46, 204, 113, 0.12); border-color: rgba(46, 204, 113, 0.3); color: #2ECC71;'>{s.upper()}</span>" for s in detailed_recs['found_skills']])
                    st.markdown(found_html, unsafe_allow_html=True)
                else:
                    st.markdown("<span style='color:gray; font-size:0.85rem;'>None matched yet.</span>", unsafe_allow_html=True)
                
                # Missing Required
                st.markdown("<br><b style='color: #FF5252;'>Missing Required Skills:</b><br>", unsafe_allow_html=True)
                if detailed_recs['missing_required']:
                    missing_req_html = "".join([f"<span class='gap-tag' style='background: rgba(255, 82, 82, 0.12); border-color: rgba(255, 82, 82, 0.3); color: #FF5252;'>{s.upper()}</span>" for s in detailed_recs['missing_required']])
                    st.markdown(missing_req_html, unsafe_allow_html=True)
                else:
                    st.success("All required skills found!")
                
                # Missing Advanced
                st.markdown("<br><b style='color: #9D4EDD;'>Missing Advanced Skills (Differentiators):</b><br>", unsafe_allow_html=True)
                if detailed_recs['missing_advanced']:
                    missing_adv_html = "".join([f"<span class='skill-tag' style='background: rgba(157, 78, 221, 0.12); border-color: rgba(157, 78, 221, 0.3); color: #9D4EDD;'>{s.upper()}</span>" for s in detailed_recs['missing_advanced']])
                    st.markdown(missing_adv_html, unsafe_allow_html=True)
                else:
                    st.markdown("<span style='color:gray; font-size:0.85rem;'>No further advanced gaps.</span>", unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)

            with col2:
                st.markdown("<h4>💡 AI Learning Path Recommendation</h4>", unsafe_allow_html=True)
                
                if detailed_recs['matching_percentage'] == 100 and not detailed_recs['missing_advanced']:
                    st.markdown(f"""
                    <div class="rec-item" style="border-left-color: #00E5FF;">
                        ✨ <b>Outstanding {detailed_recs['role_name']} Profile!</b> You have perfectly matched all benchmark requirements and advanced differentiators. Focus on deep system architecture, writing open-source modules, or publishing industry research.
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("<h5>🛣️ Step-by-Step Skill Acquisition Roadmap</h5>", unsafe_allow_html=True)
                    for item in detailed_recs['roadmap']:
                        st.markdown(f"""
                        <div class="rec-item" style="border-left-color: #00E5FF;">
                            {item}
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("<br><h5>🛠️ High-Impact Hands-on Projects</h5>", unsafe_allow_html=True)
                    for proj in detailed_recs['projects']:
                        st.markdown(f"""
                        <div class="rec-item" style="border-left-color: #7B2CBF; background: rgba(123, 44, 191, 0.03);">
                            {proj}
                        </div>
                        """, unsafe_allow_html=True)
                        
                st.markdown("<br><p style='color: #A0AEC0; font-size: 0.9rem;'><i>* Recommendations are custom-generated by matching the candidate's extracted profile against expert industry benchmarks for the selected role.</i></p>", unsafe_allow_html=True)
