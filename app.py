import streamlit as st
import pandas as pd
import altair as alt
import plotly.graph_objects as go
from fpdf import FPDF
import joblib
import os
from logic import analyze_career_data

# --- UI CONFIGURATION ---
st.set_page_config(
    page_title="DataSight Analytics", 
    page_icon="📈", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- SESSION STATE INITIALIZATION ---
if "result" not in st.session_state:
    st.session_state.result = None
if "current_sal" not in st.session_state:
    st.session_state.current_sal = None
if "target_sal" not in st.session_state:
    st.session_state.target_sal = None

# --- PREMIUM SAAS CSS INJECTION ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }
    .stApp { background-color: #0F172A !important; }
    #MainMenu { visibility: hidden !important; }
    footer { visibility: hidden !important; }
    .block-container { padding-top: 2rem !important; padding-bottom: 2rem !important; }
    h1, h2, h3, h4, h5, h6, p, span, label, div { color: #F8FAFC !important; }
    [data-testid="stSidebar"] { background-color: #1E293B !important; border-right: 1px solid #334155 !important; }
    [data-testid="metric-container"] {
        background-color: #1E293B !important;
        border: 1px solid #334155 !important;
        padding: 24px 20px !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06) !important;
    }
    [data-testid="stMetricLabel"] > div { color: #94A3B8 !important; font-size: 1rem !important; font-weight: 400 !important; }
    [data-testid="stMetricValue"] > div { color: #F8FAFC !important; font-size: 2.2rem !important; font-weight: 700 !important; }
    .stTextArea textarea {
        background-color: #0F172A !important;
        border: 1px solid #334155 !important;
        color: #F8FAFC !important;
        border-radius: 8px !important;
        padding: 12px !important;
    }
    .stTextArea textarea:focus { border-color: #6366F1 !important; box-shadow: 0 0 0 1px #6366F1 !important; }
    div.stButton > button, div.stDownloadButton > button {
        background-color: #6366F1 !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px !important;
        padding: 0.5rem 1rem !important;
        transition: all 0.2s ease !important;
        width: 100% !important;
    }
    div.stButton > button:hover, div.stDownloadButton > button:hover {
        background-color: #4F46E5 !important;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3) !important;
        transform: translateY(-2px);
    }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; border-bottom: 1px solid #334155; }
    .stTabs [data-baseweb="tab"] { padding: 12px 4px; color: #94A3B8 !important; background-color: transparent !important; }
    .stTabs [aria-selected="true"] { color: #F8FAFC !important; border-bottom: 2px solid #6366F1 !important; }
    .stAlert { background-color: #1E293B !important; border: 1px solid #334155 !important; border-radius: 8px !important; }
    hr { border-color: #334155 !important; }
</style>
""", unsafe_allow_html=True)

# --- PDF GENERATOR ---
def generate_pdf(result, current_sal, target_sal):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("helvetica", size=10)
    pdf.set_font("helvetica", 'B', 16)
    pdf.cell(0, 10, "DataSight Executive Career Report", ln=True, align='C')
    pdf.ln(5)
    pdf.set_font("helvetica", size=11)
    pdf.cell(0, 8, f"Total Job Nodes Scanned: {result['total_jobs_analyzed']:,}", ln=True)
    pdf.cell(0, 8, f"Competitiveness Index: {result['match_percentage']}%", ln=True)
    pdf.ln(5)
    pdf.set_font("helvetica", 'B', 12)
    pdf.cell(0, 8, "CURRENT ASSETS:", ln=True)
    pdf.set_font("helvetica", size=11)
    assets = ', '.join([format_skill(s) for s in result['matched_skills']]) if result['matched_skills'] else 'None matching top market demands.'
    pdf.multi_cell(0, 8, assets)
    pdf.ln(5)
    pdf.set_font("helvetica", 'B', 12)
    pdf.cell(0, 8, "CRITICAL DEFICITS (PRIORITY UPSKILLING):", ln=True)
    pdf.set_font("helvetica", size=11)
    deficits = ', '.join([format_skill(s) for s in result['missing_skills']]) if result['missing_skills'] else 'None.'
    pdf.multi_cell(0, 8, deficits)
    pdf.ln(5)
    pdf.set_font("helvetica", 'B', 12)
    pdf.cell(0, 8, "FINANCIAL PROJECTIONS (AI DRIVEN):", ln=True)
    pdf.set_font("helvetica", size=11)
    pdf.cell(0, 8, f"Predicted Market Value: {current_sal}", ln=True)
    pdf.cell(0, 8, f"Target Value (Post-Upskilling): {target_sal}", ln=True)
    pdf.ln(5)
    pdf.set_font("helvetica", 'B', 12)
    pdf.cell(0, 8, "TOP HIRING TARGETS:", ln=True)
    pdf.set_font("helvetica", size=11)
    companies = ', '.join([c.title() for c in result['top_companies']]) if result['top_companies'] else 'Insufficient data.'
    pdf.multi_cell(0, 8, companies)
    return bytes(pdf.output())

# --- SPEED OPTIMIZATION & AI CACHING ---
@st.cache_data
def run_analysis(dataset_path, user_skills, wfh):
    return analyze_career_data(dataset_path, user_skills, wfh)

@st.cache_resource
def load_ai_brain():
    try:
        model = joblib.load("salary_model.pkl")
        features = joblib.load("model_features.pkl")
        return model, features
    except FileNotFoundError:
        return None, None

def format_skill(skill):
    acronyms = ["sql", "aws", "gcp", "r", "api", "bi"]
    words = skill.split()
    return " ".join([w.upper() if w.lower() in acronyms else w.title() for w in words])

# --- SIDEBAR CONTROLS ---
with st.sidebar:
    st.markdown("<h2 style='color: #F8FAFC;'>DataSight Analytics</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94A3B8; font-size: 0.9rem;'>Algorithmic Career Intelligence</p>", unsafe_allow_html=True)
    st.write("")
    st.markdown("<label style='font-weight: 600; font-size: 0.95rem; color: #E2E8F0;'>Current Technology Stack</label>", unsafe_allow_html=True)
    user_skills_input = st.text_area("", placeholder="e.g., Python, SQL, Tableau, AWS...", height=120, label_visibility="collapsed")
    wfh_only = st.toggle("Isolate Remote (WFH) Roles")
    st.write("")
    analyze_btn = st.button("Initialize Data Scan")

# --- MAIN DASHBOARD AREA ---
if not st.session_state.result and not analyze_btn:
    st.markdown("<h1 style='font-size: 2.5rem; margin-bottom: 0;'>Market Analysis Output</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94A3B8; font-size: 1.1rem;'>Easily compare your technological profile against real-time job market requirements.</p>", unsafe_allow_html=True)
    st.write("")
    st.info("👈 System Standby: Please input your technology stack in the sidebar to begin analysis.")

# --- CORE ENGINE & ML PIPELINE ---
if analyze_btn:
    if not user_skills_input:
        st.warning("⚠️ Parameter Missing: Please define your technology stack in the sidebar.")
    else:
        with st.spinner("Executing distributed dataset scan & AI Prediction..."):
            st.session_state.result = run_analysis("dataset.csv", user_skills_input, wfh_only)
            
            if st.session_state.result["status"] != "error":
                res = st.session_state.result
                ai_model, ai_features = load_ai_brain()
                
                if ai_model and ai_features:
                    cols = ai_features + ['work_from_home']
                    curr_data = {c: 0 for c in cols}
                    curr_data['work_from_home'] = int(wfh_only)
                    for s in res['matched_skills']:
                        if s.lower() in ai_features:
                            curr_data[s.lower()] = 1
                            
                    targ_data = curr_data.copy()
                    if res['missing_skills']:
                        top_missing = res['missing_skills'][0].lower()
                        if top_missing in ai_features:
                            targ_data[top_missing] = 1
                            
                    df_curr = pd.DataFrame([curr_data], columns=cols)
                    df_targ = pd.DataFrame([targ_data], columns=cols)
                    
                    ai_curr = ai_model.predict(df_curr)[0]
                    ai_targ = ai_model.predict(df_targ)[0]
                    
                    # --- ENTERPRISE UX SAFEGUARD ---
                    # Prevents the AI from showing negative ROI if statistical
                    # dataset quirks associate a new skill with a lower-paying job tier.
                    if ai_targ < ai_curr:
                        ai_targ = ai_curr
                        
                    st.session_state.current_sal = f"${ai_curr:,.0f} (AI)"
                    st.session_state.target_sal = f"${ai_targ:,.0f} (AI)"
                else:
                    st.session_state.current_sal = f"${res['market_salary']:,.0f}" if not pd.isna(res['market_salary']) else "N/A"
                    st.session_state.target_sal = f"${res['target_salary']:,.0f}" if not pd.isna(res['target_salary']) else "N/A"

# --- RENDER DASHBOARD ---
if st.session_state.result and analyze_btn or st.session_state.result:
    result = st.session_state.result
    
    if result["status"] == "error":
        st.error(result["message"])
    else:
        st.markdown("<h1 style='font-size: 2.5rem; margin-bottom: 0;'>Market Analysis Output</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color: #94A3B8; font-size: 1.1rem; margin-bottom: 2rem;'>Algorithmic skill-gap analysis cross-referenced with live market constraints.</p>", unsafe_allow_html=True)
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Market Competitiveness", f"{result['match_percentage']}%")
        current_sal = st.session_state.current_sal
        target_sal = st.session_state.target_sal
        
        try:
            curr_val = float(current_sal.replace('$', '').replace(',', '').replace(' (AI)', ''))
            targ_val = float(target_sal.replace('$', '').replace(',', '').replace(' (AI)', ''))
            boost = targ_val - curr_val
            boost_str = f"+${boost:,.0f} ROI" if boost > 0 else "Baseline"
        except:
            boost_str = "Baseline"
            
        m2.metric("Predicted Market Value", current_sal)
        m3.metric("Projected Target Value", target_sal, delta=boost_str)
        
        st.write("")
        st.write("")
        
        # --- MULTI-DIMENSIONAL DATA VISUALIZATION ---
        st.markdown("### Structural Market Mapping")
        
        # Creating a 2-Column Layout for the Charts
        chart_col1, chart_col2 = st.columns([1.2, 1])
        
        with chart_col1:
            st.markdown("<p style='color: #94A3B8; font-size: 0.9rem;'>Frequency Distribution (Top 10)</p>", unsafe_allow_html=True)
            chart_df = pd.DataFrame(list(result['top_skills_dict'].items()), columns=['Technology', 'Market Mentions']).head(10)
            chart_df['Technology'] = chart_df['Technology'].apply(format_skill)
            
            bar_chart = alt.Chart(chart_df).mark_bar(
                color='#6366F1', opacity=0.9, cornerRadiusTopLeft=6, cornerRadiusTopRight=6, size=30 
            ).encode(
                x=alt.X('Technology:N', sort='-y', title="", axis=alt.Axis(labelColor='#94A3B8', labelAngle=-45, grid=False)),
                y=alt.Y('Market Mentions:Q', title="Mentions", axis=alt.Axis(labelColor='#94A3B8', titleColor='#94A3B8', grid=True, gridColor='#334155')),
                tooltip=[alt.Tooltip('Technology:N', title='Skill'), alt.Tooltip('Market Mentions:Q', title='Mentions')]
            ).properties(height=350).configure_view(strokeWidth=0)
            st.altair_chart(bar_chart, use_container_width=True, theme=None) 

        with chart_col2:
            st.markdown("<p style='color: #94A3B8; font-size: 0.9rem;'>Competency Gap Analysis (Radar)</p>", unsafe_allow_html=True)
            
            # --- PLOTLY RADAR CHART LOGIC ---
            top_6 = list(result['top_skills_dict'].keys())[:6]
            if len(top_6) > 2: # Radar charts need at least 3 points to look good
                market_freq = [result['top_skills_dict'][s] for s in top_6]
                max_freq = max(market_freq) if market_freq else 1
                market_scores = [(f / max_freq) * 100 for f in market_freq]
                
                user_scores = []
                for s in top_6:
                    if s in result['matched_skills']:
                        user_scores.append((result['top_skills_dict'][s] / max_freq) * 100)
                    else:
                        user_scores.append(0)
                        
                # Close the loop for the web
                top_6.append(top_6[0])
                market_scores.append(market_scores[0])
                user_scores.append(user_scores[0])
                formatted_skills = [format_skill(s) for s in top_6]

                fig = go.Figure()
                fig.add_trace(go.Scatterpolar(
                    r=market_scores, theta=formatted_skills, fill='toself', 
                    name='Market Demand', line_color='#475569', fillcolor='rgba(71, 85, 105, 0.2)'
                ))
                fig.add_trace(go.Scatterpolar(
                    r=user_scores, theta=formatted_skills, fill='toself', 
                    name='Your Profile', line_color='#6366F1', fillcolor='rgba(99, 102, 241, 0.6)'
                ))
                fig.update_layout(
                    polar=dict(
                        radialaxis=dict(visible=False, range=[0, 100]),
                        angularaxis=dict(color='#F8FAFC', gridcolor='#334155'),
                        bgcolor='rgba(0,0,0,0)'
                    ),
                    showlegend=True, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                    margin=dict(l=40, r=40, t=20, b=20),
                    legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5, font=dict(color="#94A3B8"))
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.write("*Insufficient data points for a radar projection.*")
        
        st.write("")
        
        # --- TABS ---
        tab1, tab2, tab3 = st.tabs(["Competency Deficits", "Active Hiring Entities", "Export Strategy"])
        with tab1:
            st.write("")
            col_matched, col_missing = st.columns(2)
            with col_matched:
                st.markdown("<h4 style='color: #F8FAFC;'>Verified Core Assets</h4>", unsafe_allow_html=True)
                if result['matched_skills']:
                    for skill in result['matched_skills']:
                        st.markdown(f"<p style='color: #10B981; font-weight: 600;'>✓ {format_skill(skill)}</p>", unsafe_allow_html=True)
                else:
                    st.write("*No exact matches detected within the top percentile.*")
            with col_missing:
                st.markdown("<h4 style='color: #F8FAFC;'>Identified Skill Deficits</h4>", unsafe_allow_html=True)
                if result['missing_skills']:
                    for skill in result['missing_skills']:
                        st.markdown(f"<p style='color: #EF4444; font-weight: 600;'>⚠ {format_skill(skill)}</p>", unsafe_allow_html=True)
                else:
                    st.write("Profile is perfectly aligned with maximum market demand.")
                    
        with tab2:
            st.write("")
            st.markdown("#### Organizations prioritizing your competency cluster:")
            st.write("")
            if result['top_companies']:
                for i, company in enumerate(result['top_companies']):
                    st.markdown(f"**{i+1}. {company.title()}**")
            else:
                st.write("*Insufficient data for target organization extraction.*")
                
        with tab3:
            st.write("")
            st.markdown("#### Download Strategic Blueprint")
            st.write("Export your personalized, data-driven career strategy as a formatted PDF.")
            pdf_bytes = generate_pdf(result, current_sal, target_sal)
            st.download_button(label="Export Data Report (.PDF)", data=pdf_bytes, file_name="DataSight_Executive_Report.pdf", mime="application/pdf")