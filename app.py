import streamlit as st
import pandas as pd
import altair as alt
from fpdf import FPDF
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
    /* Import Premium Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    /* Global App Background & Typography */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
    }
    .stApp {
        background-color: #0F172A !important; /* Deep Slate Background */
    }
    
    /* STABILITY FIX: Safely hide only the footer and main menu, leaving the header and sidebar toggle completely intact */
    #MainMenu { visibility: hidden !important; }
    footer { visibility: hidden !important; }
    
    /* Adjust Top Padding */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
    }

    /* Global Text Colors */
    h1, h2, h3, h4, h5, h6, p, span, label, div {
        color: #F8FAFC !important; /* Crisp White Text */
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #1E293B !important; /* Slightly lighter slate */
        border-right: 1px solid #334155 !important;
    }
    
    /* Metric Cards (The "Glass" Look) */
    [data-testid="metric-container"] {
        background-color: #1E293B !important;
        border: 1px solid #334155 !important;
        padding: 24px 20px !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06) !important;
    }
    [data-testid="stMetricLabel"] > div {
        color: #94A3B8 !important; /* Muted subtitle */
        font-size: 1rem !important;
        font-weight: 400 !important;
    }
    [data-testid="stMetricValue"] > div {
        color: #F8FAFC !important;
        font-size: 2.2rem !important;
        font-weight: 700 !important;
    }
    
    /* Input Fields (Text Area) */
    .stTextArea textarea {
        background-color: #0F172A !important;
        border: 1px solid #334155 !important;
        color: #F8FAFC !important;
        border-radius: 8px !important;
        padding: 12px !important;
    }
    .stTextArea textarea:focus {
        border-color: #6366F1 !important; /* Indigo Focus */
        box-shadow: 0 0 0 1px #6366F1 !important;
    }
    
    /* Primary Buttons (Analyze & Download) */
    div.stButton > button, div.stDownloadButton > button {
        background-color: #6366F1 !important; /* Indigo Accent */
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px !important;
        padding: 0.5rem 1rem !important;
        transition: all 0.2s ease !important;
        width: 100% !important;
    }
    div.stButton > button p, div.stDownloadButton > button p {
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }
    div.stButton > button:hover, div.stDownloadButton > button:hover {
        background-color: #4F46E5 !important; /* Darker Indigo on hover */
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3) !important;
        transform: translateY(-2px);
    }
    
    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] { 
        gap: 24px;
        border-bottom: 1px solid #334155;
    }
    .stTabs [data-baseweb="tab"] { 
        padding: 12px 4px;
        color: #94A3B8 !important;
        background-color: transparent !important;
    }
    .stTabs [aria-selected="true"] {
        color: #F8FAFC !important;
        border-bottom: 2px solid #6366F1 !important; /* Indigo underline */
    }
    
    /* Alerts and Info Boxes */
    .stAlert {
        background-color: #1E293B !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
        color: #F8FAFC !important;
    }
    
    /* Dividers */
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
    pdf.cell(0, 8, "FINANCIAL PROJECTIONS:", ln=True)
    pdf.set_font("helvetica", size=11)
    pdf.cell(0, 8, f"Median Market Value: {current_sal}", ln=True)
    pdf.cell(0, 8, f"Target Value (Post-Upskilling): {target_sal}", ln=True)
    pdf.ln(5)
    pdf.set_font("helvetica", 'B', 12)
    pdf.cell(0, 8, "TOP HIRING TARGETS:", ln=True)
    pdf.set_font("helvetica", size=11)
    companies = ', '.join([c.title() for c in result['top_companies']]) if result['top_companies'] else 'Insufficient data.'
    pdf.multi_cell(0, 8, companies)
    return bytes(pdf.output())


# --- SPEED OPTIMIZATION ---
@st.cache_data
def run_analysis(dataset_path, user_skills, wfh):
    return analyze_career_data(dataset_path, user_skills, wfh)


def format_skill(skill):
    acronyms = ["sql", "aws", "gcp", "r", "api", "bi"]
    words = skill.split()
    formatted_words = [w.upper() if w.lower() in acronyms else w.title() for w in words]
    return " ".join(formatted_words)


# --- SIDEBAR CONTROLS ---
with st.sidebar:
    st.markdown("<h2 style='color: #F8FAFC;'>DataSight Analytics</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94A3B8; font-size: 0.9rem;'>Algorithmic Career Intelligence</p>", unsafe_allow_html=True)
    st.write("")
    st.write("")
    
    st.markdown("<label style='font-weight: 600; font-size: 0.95rem; color: #E2E8F0;'>Current Technology Stack</label>", unsafe_allow_html=True)
    user_skills_input = st.text_area("", placeholder="e.g., Python, SQL, Tableau, AWS...", height=120, label_visibility="collapsed")
    
    st.write("")
    wfh_only = st.toggle("Isolate Remote (WFH) Roles")
    
    st.write("")
    st.write("")
    analyze_btn = st.button("Initialize Data Scan")


# --- MAIN DASHBOARD AREA ---
if not st.session_state.result and not analyze_btn:
    st.markdown("<h1 style='font-size: 2.5rem; margin-bottom: 0;'>Market Analysis Output</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94A3B8; font-size: 1.1rem;'>Easily compare your technological profile against real-time job market requirements.</p>", unsafe_allow_html=True)
    st.write("")
    st.info("👈 System Standby: Please input your technology stack in the sidebar to begin analysis.")


# If button is clicked, update the session state
if analyze_btn:
    if not user_skills_input:
        st.warning("⚠️ Parameter Missing: Please define your technology stack in the sidebar.")
    else:
        with st.spinner("Executing distributed dataset scan..."):
            st.session_state.result = run_analysis("dataset.csv", user_skills_input, wfh_only)
            
            if st.session_state.result["status"] != "error":
                res = st.session_state.result
                st.session_state.current_sal = f"${res['market_salary']:,.0f}" if not pd.isna(res['market_salary']) else "N/A"
                st.session_state.target_sal = f"${res['target_salary']:,.0f}" if not pd.isna(res['target_salary']) else "N/A"


# --- RENDER DASHBOARD (Only if data exists in memory) ---
if st.session_state.result and analyze_btn or st.session_state.result:
    result = st.session_state.result
    
    if result["status"] == "error":
        st.error(result["message"])
    else:
        # Title
        st.markdown("<h1 style='font-size: 2.5rem; margin-bottom: 0;'>Market Analysis Output</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color: #94A3B8; font-size: 1.1rem; margin-bottom: 2rem;'>Algorithmic skill-gap analysis cross-referenced with live market constraints.</p>", unsafe_allow_html=True)
        
        # --- TOP LEVEL METRICS ---
        m1, m2, m3 = st.columns(3)
        m1.metric("Market Competitiveness", f"{result['match_percentage']}%")
        
        current_sal = st.session_state.current_sal
        target_sal = st.session_state.target_sal
        
        if not pd.isna(result['target_salary']) and not pd.isna(result['market_salary']):
            boost = result['target_salary'] - result['market_salary']
            boost_str = f"+${boost:,.0f} ROI" if boost > 0 else "Baseline"
        else:
            boost_str = "Baseline"
        
        m2.metric("Median Market Compensation", current_sal)
        m3.metric("Projected Target Compensation", target_sal, delta=boost_str)
        
        st.write("")
        st.write("")
        
        # --- INTERACTIVE DATA VISUALIZATION ---
        chart_df = pd.DataFrame(list(result['top_skills_dict'].items()), columns=['Technology', 'Market Mentions'])
        chart_df['Technology'] = chart_df['Technology'].apply(format_skill)
        
        # Sleek, grid-less Altair Chart - SAFELY FORMATTED
        chart = alt.Chart(chart_df).mark_bar(
            color='#6366F1', 
            opacity=0.9, 
            cornerRadiusTopLeft=6, 
            cornerRadiusTopRight=6,
            size=45 
        ).encode(
            x=alt.X('Technology:N', sort='-y', title="", axis=alt.Axis(labelColor='#94A3B8', labelAngle=-45, labelFontSize=13, grid=False)),
            y=alt.Y('Market Mentions:Q', title="Frequency in Job Postings", axis=alt.Axis(labelColor='#94A3B8', titleColor='#94A3B8', grid=True, gridColor='#334155', gridOpacity=0.4)),
            tooltip=[alt.Tooltip('Technology:N', title='Skill'), alt.Tooltip('Market Mentions:Q', title='Mentions')]
        ).properties(height=400).configure_view(strokeWidth=0)
        
        st.altair_chart(chart, use_container_width=True, theme=None) 
        
        st.write("")
        
        # --- DEEP DIVE TABS ---
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
            
            st.download_button(
                label="Export Data Report (.PDF)",
                data=pdf_bytes,
                file_name="DataSight_Executive_Report.pdf",
                mime="application/pdf"
            )