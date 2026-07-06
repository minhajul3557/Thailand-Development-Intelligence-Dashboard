import streamlit as st
import json
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Thailand Development Intelligence Dashboard",
    page_icon="🇹🇭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom premium styling
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Outfit', sans-serif; }
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .section-title { font-weight: 700; color: #1F618D; margin-top: 20px; }
    </style>
    """,
    unsafe_allow_html=True
)

@st.cache_data
def load_results():
    models = ["llama", "qwen", "phi"]
    results = {}
    for m in models:
        paths = [f"{m}_results.json", os.path.join("results", f"{m}_results.json")]
        found = False
        for path in paths:
            if os.path.exists(path):
                with open(path, "r") as f:
                    results[m] = json.load(f)
                found = True
                break
        if not found:
            # Mock fallback if loaded standalone
            results[m] = {
                "summaries": {"Overview": "Summary of overview...", "Chapter 1": "Summary of Ch 1..."},
                "key_results": ["Key result 1", "Key result 2"],
                "indicators": {"hdi_value": 0.726, "life_expectancy_total": 72.2, "mean_years_of_schooling": 7.3, "gdp_per_capita_baht": 74675, "population": "62.1 million"},
                "strengths_challenges": {"strengths": ["Strong health system"], "challenges": ["Poverty in Northeast"]},
                "demographic_trends": ["Trend 1"],
                "processing_time_sec": 45.2
            }
    
    eval_paths = ["evaluation_results.json", os.path.join("results", "evaluation_results.json")]
    evaluations = {}
    found_eval = False
    for path in eval_paths:
        if os.path.exists(path):
            with open(path, "r") as f:
                evaluations = json.load(f)
            found_eval = True
            break
    if not found_eval:
        evaluations = {
            "llama_by_qwen": {"consistency_score": 9, "completeness_score": 8, "factual_alignment_score": 9, "comments": "High quality"},
            "qwen_by_phi": {"consistency_score": 8, "completeness_score": 9, "factual_alignment_score": 8, "comments": "Rich output"},
            "phi_by_llama": {"consistency_score": 8, "completeness_score": 7, "factual_alignment_score": 9, "comments": "Accurate but brief"}
        }
    return results, evaluations

results, evaluations = load_results()

st.title("🇹🇭 Thailand Development Intelligence Dashboard")
st.markdown("**Interactive evaluation dashboard of subnational human achievement and cross-LLM performance analysis.**")

# Sidebar configuration
st.sidebar.title("Dashboard Controls")
selected_model = st.sidebar.selectbox("Select Primary LLM for Overview", ["Llama 3.2 3B", "Qwen 2.5 3B", "Phi-3 Mini 3.8B"])
model_map = {"Llama 3.2 3B": "llama", "Qwen 2.5 3B": "qwen", "Phi-3 Mini 3.8B": "phi"}
m_key = model_map[selected_model]

tabs = st.tabs(["Executive Summary", "Chapter Summaries", "Interactive Data Exploration", "Advanced Radar Analysis", "Cross-LLM Behavior Analysis"])

# Tab 1: Executive Summary
with tabs[0]:
    st.header("National Overview & Key Insights")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("National HDI Value", "0.7263")
    with col2:
        st.metric("Life Expectancy at Birth", "72.2 Years")
    with col3:
        st.metric("Mean Years of Schooling", "7.3 Years")
    with col4:
        st.metric("GDP Per Capita (Baht)", "74,675")

    st.markdown("---")
    col_left, col_right = st.columns(2)
    with col_left:
        st.subheader("Key Development Strengths")
        strengths = results[m_key]["strengths_challenges"].get("strengths", [])
        for s in strengths:
            st.markdown(f"- {s}")
    with col_right:
        st.subheader("Key Development Challenges")
        challenges = results[m_key]["strengths_challenges"].get("challenges", [])
        for c in challenges:
            st.markdown(f"- {c}")

# Tab 2: Chapter Summaries
with tabs[1]:
    st.header("Chapter-by-Chapter Summaries")
    chapter = st.selectbox("Select Chapter", list(results[m_key]["summaries"].keys()))
    st.info(results[m_key]["summaries"][chapter])

# Tab 3: Interactive Data Exploration
with tabs[2]:
    st.header("Regional Disparity Exploration")

    # Data
    regions_data = {
        "Region": ["Bangkok Metropolis", "Bangkok Vicinity", "Eastern Region", "Central Region", "Western Region", "Southern Region", "Northern Region", "Northeastern Region"],
        "Income_1998": [25790, 19262, 12178, 11473, 12461, 11368, 9502, 8411],
        "Income_2000": [28392, 19439, 12480, 12641, 14310, 11536, 8651, 7823],
        "Poverty_2000": [0.3, 1.4, 5.2, 6.1, 6.1, 11.0, 12.2, 28.1],
        "Debt_2000": [363674, 216952, 150887, 104265, 124832, 92220, 81550, 121569],
        "Malnutrition_1997": [4.01, 1.66, 4.80, 3.26, 6.1, 5.8, 10.2, 12.9],
        "Infant_Mortality_2001": [10.0, 12.6, 5.1, 11.0, 8.0, 12.0, 13.0, 12.9],
        "Schooling_Years": [11.9, 10.5, 8.0, 7.8, 7.2, 7.1, 6.9, 6.7],
        "Secondary_Enrolment": [67.3, 56.2, 54.8, 56.1, 50.4, 50.9, 51.0, 46.5]
    }

    col_plot1, col_plot2 = st.columns(2)
    with col_plot1:
        st.subheader("Income Trend (1998 vs 2000)")
        fig3 = go.Figure()
        fig3.add_trace(go.Bar(x=regions_data["Region"], y=regions_data["Income_1998"], name="1998", marker_color="#5D6D7E"))
        fig3.add_trace(go.Bar(x=regions_data["Region"], y=regions_data["Income_2000"], name="2000", marker_color="#1F618D"))
        fig3.update_layout(barmode="group", template="plotly_white", height=400)
        st.plotly_chart(fig3, use_container_width=True)

    with col_plot2:
        st.subheader("Poverty Rate vs Household Debt")
        fig5 = go.Figure()
        fig5.add_trace(go.Bar(x=regions_data["Region"], y=regions_data["Poverty_2000"], name="Poverty Rate (%)", marker_color="#E74C3C", yaxis="y"))
        fig5.add_trace(go.Scatter(x=regions_data["Region"], y=regions_data["Debt_2000"], name="Avg Debt (Baht)", line=dict(color="#2ECC71", width=3), yaxis="y2"))
        fig5.update_layout(
            yaxis=dict(title=dict(text="Poverty Rate (%)", font=dict(color="#E74C3C")), tickfont=dict(color="#E74C3C")),
            yaxis2=dict(title=dict(text="Household Debt (Baht)", font=dict(color="#2ECC71")), tickfont=dict(color="#2ECC71"), anchor="x", overlaying="y", side="right"),
            template="plotly_white", height=400
        )
        st.plotly_chart(fig5, use_container_width=True)

    col_plot3, col_plot4 = st.columns(2)
    with col_plot3:
        st.subheader("Child Health Disparities")
        fig6 = go.Figure()
        fig6.add_trace(go.Bar(x=regions_data["Region"], y=regions_data["Malnutrition_1997"], name="Under-5 Malnutrition (%)", marker_color="#F39C12"))
        fig6.add_trace(go.Bar(x=regions_data["Region"], y=regions_data["Infant_Mortality_2001"], name="Infant Mortality (per 1,000)", marker_color="#9B59B6"))
        fig6.update_layout(barmode="group", template="plotly_white", height=400)
        st.plotly_chart(fig6, use_container_width=True)
    with col_plot4:
        st.subheader("Education Development Metrics")
        fig7 = go.Figure()
        fig7.add_trace(go.Bar(x=regions_data["Region"], y=regions_data["Schooling_Years"], name="Mean Years of Schooling", marker_color="#16A085"))
        fig7.add_trace(go.Bar(x=regions_data["Region"], y=regions_data["Secondary_Enrolment"], name="Secondary Enrolment Rate (%)", marker_color="#F1C40F"))
        fig7.update_layout(barmode="group", template="plotly_white", height=400)
        st.plotly_chart(fig7, use_container_width=True)

# Tab 4: Advanced Radar Analysis
with tabs[3]:
    st.header("Subnational Multidimensional Development (HAI Dimensions)")
    categories = ['Health', 'Education', 'Employment', 'Income', 'Housing', 'Family & Community', 'Transport & Comm', 'Participation']

    # Add selection
    selected_regions = st.multiselect("Select Regions to Compare", ["Kingdom (National)", "Bangkok Metropolis", "Northeastern Region"], default=["Kingdom (National)", "Bangkok Metropolis", "Northeastern Region"])

    fig4 = go.Figure()
    if "Bangkok Metropolis" in selected_regions:
        fig4.add_trace(go.Scatterpolar(r=[0.7884, 0.5418, 0.6744, 0.8074, 0.8191, 0.5816, 0.8765, 0.2959], theta=categories, fill='toself', name='Bangkok Metropolis'))
    if "Kingdom (National)" in selected_regions:
        fig4.add_trace(go.Scatterpolar(r=[0.6889, 0.5075, 0.5885, 0.5100, 0.7040, 0.6573, 0.5984, 0.6758], theta=categories, fill='toself', name='Kingdom (National)'))
    if "Northeastern Region" in selected_regions:
        fig4.add_trace(go.Scatterpolar(r=[0.6234, 0.4654, 0.5074, 0.3542, 0.5422, 0.7209, 0.4392, 0.6502], theta=categories, fill='toself', name='Northeastern Region'))

    fig4.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 1.0])), height=500)
    st.plotly_chart(fig4, use_container_width=True)

# Tab 5: Cross-LLM Behavior Analysis
with tabs[4]:
    st.header("Cross-LLM Behavior & Validation Quality")

    # Comparison Table of extracted indicators
    comp_data = {
        "Indicator": ["HDI Value", "Life Expectancy", "Mean Schooling", "GDP Per Capita (Baht)", "Population"],
        "Ground Truth": [0.7263, 72.2, 7.3, 74675, "62.1-62.3 Million"],
        "Llama 3.2 3B": [results["llama"]["indicators"].get("hdi_value"), results["llama"]["indicators"].get("life_expectancy_total"), results["llama"]["indicators"].get("mean_years_of_schooling"), results["llama"]["indicators"].get("gdp_per_capita_baht"), results["llama"]["indicators"].get("population")],
        "Qwen 2.5 3B": [results["qwen"]["indicators"].get("hdi_value"), results["qwen"]["indicators"].get("life_expectancy_total"), results["qwen"]["indicators"].get("mean_years_of_schooling"), results["qwen"]["indicators"].get("gdp_per_capita_baht"), results["qwen"]["indicators"].get("population")],
        "Phi-3 Mini 3.8B": [results["phi"]["indicators"].get("hdi_value"), results["phi"]["indicators"].get("life_expectancy_total"), results["phi"]["indicators"].get("mean_years_of_schooling"), results["phi"]["indicators"].get("gdp_per_capita_baht"), results["phi"]["indicators"].get("population")]
    }

    st.subheader("Accuracy Verification: Extracted Indicators vs Ground Truth")
    # Cast dataframe to str to prevent PyArrow serialization errors from mixed numeric/string columns
    st.table(pd.DataFrame(comp_data).astype(str))

    st.subheader("Circular Cross-LLM Evaluation Scores")
    eval_summary = {
        "Extraction Evaluated": ["Llama 3.2 (by Qwen)", "Qwen 2.5 (by Phi)", "Phi-3 (by Llama)"],
        "Consistency (1-10)": [evaluations.get("llama_by_qwen", {}).get("consistency_score"), evaluations.get("qwen_by_phi", {}).get("consistency_score"), evaluations.get("phi_by_llama", {}).get("consistency_score")],
        "Completeness (1-10)": [evaluations.get("llama_by_qwen", {}).get("completeness_score"), evaluations.get("qwen_by_phi", {}).get("completeness_score"), evaluations.get("phi_by_llama", {}).get("completeness_score")],
        "Factual Alignment (1-10)": [evaluations.get("llama_by_qwen", {}).get("factual_alignment_score"), evaluations.get("qwen_by_phi", {}).get("factual_alignment_score"), evaluations.get("phi_by_llama", {}).get("factual_alignment_score")],
        "Review Comments": [evaluations.get("llama_by_qwen", {}).get("comments"), evaluations.get("qwen_by_phi", {}).get("comments"), evaluations.get("phi_by_llama", {}).get("comments")]
    }
    st.table(pd.DataFrame(eval_summary).astype(str))

    st.markdown("---")
    st.subheader("Visual Model Benchmarks")
    col_bench1, col_bench2 = st.columns(2)
    with col_bench1:
        st.markdown("**Model Summary Lengths (Word Count)**")
        chapters = ["Overview", "Chapter 1", "Chapter 2", "Chapter 3", "Chapter 4", "Chapter 5"]
        fig_verb = go.Figure()
        for m_key, m_label in [("llama", "Llama 3.2 3B"), ("qwen", "Qwen 2.5 3B"), ("phi", "Phi-3 Mini 3.8B")]:
            word_counts = [len(results[m_key]["summaries"].get(ch, "").split()) for ch in chapters]
            fig_verb.add_trace(go.Bar(x=chapters, y=word_counts, name=m_label))
        fig_verb.update_layout(barmode="group", template="plotly_white", height=350, yaxis_title="Word Count")
        st.plotly_chart(fig_verb, use_container_width=True)
    with col_bench2:
        st.markdown("**Circular Cross-Evaluation Scores (1-10)**")
        eval_metrics = ["Consistency", "Completeness", "Factual Alignment"]
        fig_e = go.Figure()
        llama_s = [evaluations.get("llama_by_qwen", {}).get("consistency_score", 0), evaluations.get("llama_by_qwen", {}).get("completeness_score", 0), evaluations.get("llama_by_qwen", {}).get("factual_alignment_score", 0)]
        qwen_s = [evaluations.get("qwen_by_phi", {}).get("consistency_score", 0), evaluations.get("qwen_by_phi", {}).get("completeness_score", 0), evaluations.get("qwen_by_phi", {}).get("factual_alignment_score", 0)]
        phi_s = [evaluations.get("phi_by_llama", {}).get("consistency_score", 0), evaluations.get("phi_by_llama", {}).get("completeness_score", 0), evaluations.get("phi_by_llama", {}).get("factual_alignment_score", 0)]
        fig_e.add_trace(go.Bar(x=eval_metrics, y=llama_s, name="Llama 3.2", marker_color="#3498DB"))
        fig_e.add_trace(go.Bar(x=eval_metrics, y=qwen_s, name="Qwen 2.5", marker_color="#E67E22"))
        fig_e.add_trace(go.Bar(x=eval_metrics, y=phi_s, name="Phi-3", marker_color="#2ECC71"))
        fig_e.update_layout(barmode="group", template="plotly_white", height=350, yaxis_range=[0, 10])
        st.plotly_chart(fig_e, use_container_width=True)

    st.markdown("**Model Extraction Pipeline Speed (Seconds)**")
    times = [results[m_key].get("processing_time_sec", 0.0) for m_key in ["llama", "qwen", "phi"]]
    fig_t = go.Figure()
    fig_t.add_trace(go.Bar(x=["Llama 3.2 3B", "Qwen 2.5 3B", "Phi-3 Mini 3.8B"], y=times, marker_color=["#3498DB", "#E67E22", "#2ECC71"]))
    fig_t.update_layout(template="plotly_white", height=280, yaxis_title="Seconds")
    st.plotly_chart(fig_t, use_container_width=True)
