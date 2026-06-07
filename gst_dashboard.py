import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import base64
from pathlib import Path

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="GST Intelligence Portal",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── Custom CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --crimson:    #C0143C;
    --crimson-lt: #E8184A;
    --navy:       #0C2340;
    --navy-lt:    #1A3A5C;
    --gold:       #F0A500;
    --gold-lt:    #FFD166;
    --slate:      #1E2B3A;
    --slate-lt:   #263547;
    --mist:       #EEF2F7;
    --white:      #FFFFFF;
    --success:    #00B67A;
    --warning:    #F59E0B;
    --info:       #3B82F6;
}

html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0C2340 0%, #1A3A5C 40%, #0C2340 100%);
    font-family: 'Sora', sans-serif;
}

/* Hide default Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }
[data-testid="stSidebar"] { display: none; }

/* Main container */
.block-container {
    padding: 1.5rem 2.5rem !important;
    max-width: 1400px !important;
}

/* ─── HEADER ─── */
.portal-header {
    background: linear-gradient(120deg, #C0143C 0%, #8B0F2C 50%, #0C2340 100%);
    border-radius: 20px;
    padding: 28px 40px;
    margin-bottom: 28px;
    display: flex;
    align-items: center;
    gap: 28px;
    box-shadow: 0 20px 60px rgba(192,20,60,0.35), 0 4px 20px rgba(0,0,0,0.4);
    position: relative;
    overflow: hidden;
}
.portal-header::before {
    content: '';
    position: absolute; inset: 0;
    background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.04'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
}
.portal-title { flex: 1; }
.portal-title h1 {
    font-size: 2.2rem; font-weight: 800;
    color: #FFFFFF; margin: 0; letter-spacing: -0.5px;
    text-shadow: 0 2px 10px rgba(0,0,0,0.3);
}
.portal-title p {
    font-size: 0.95rem; color: rgba(255,255,255,0.75);
    margin: 4px 0 0; font-weight: 400;
}
.header-badge {
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 50px; padding: 8px 20px;
    color: white; font-size: 0.8rem; font-weight: 600;
    letter-spacing: 0.5px; backdrop-filter: blur(10px);
}

/* ─── GLASS CARDS ─── */
.glass-card {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 18px;
    padding: 24px;
    backdrop-filter: blur(20px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.2);
    transition: all 0.3s ease;
}
.glass-card:hover {
    border-color: rgba(192,20,60,0.4);
    box-shadow: 0 12px 40px rgba(192,20,60,0.15);
    transform: translateY(-2px);
}
.section-label {
    font-size: 0.7rem; font-weight: 700; letter-spacing: 2px;
    color: #F0A500; text-transform: uppercase; margin-bottom: 16px;
}
.section-title {
    font-size: 1.15rem; font-weight: 700;
    color: #FFFFFF; margin-bottom: 18px;
}

/* ─── RESULT CARD ─── */
.result-hero {
    background: linear-gradient(135deg, #1E2B3A 0%, #263547 100%);
    border: 1px solid rgba(240,165,0,0.3);
    border-radius: 20px; padding: 32px;
    position: relative; overflow: hidden;
    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
}
.result-hero::after {
    content: '';
    position: absolute; top: -50%; right: -50%;
    width: 100%; height: 100%;
    background: radial-gradient(circle, rgba(192,20,60,0.08) 0%, transparent 70%);
    pointer-events: none;
}
.gst-rate-circle {
    width: 130px; height: 130px;
    border-radius: 50%;
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    font-weight: 800; margin: 0 auto 20px;
    position: relative;
}
.gst-rate-nil {
    background: linear-gradient(135deg, #00B67A, #007A53);
    box-shadow: 0 8px 30px rgba(0,182,122,0.4);
}
.gst-rate-low {
    background: linear-gradient(135deg, #3B82F6, #1D4ED8);
    box-shadow: 0 8px 30px rgba(59,130,246,0.4);
}
.gst-rate-mid {
    background: linear-gradient(135deg, #F59E0B, #D97706);
    box-shadow: 0 8px 30px rgba(245,158,11,0.4);
}
.gst-rate-high {
    background: linear-gradient(135deg, #C0143C, #8B0F2C);
    box-shadow: 0 8px 30px rgba(192,20,60,0.4);
}
.rate-number { font-size: 2.4rem; color: white; line-height: 1; }
.rate-label { font-size: 0.75rem; color: rgba(255,255,255,0.8); font-weight: 500; }

.tax-breakdown-row {
    display: flex; gap: 12px; margin-top: 20px; flex-wrap: wrap;
}
.tax-pill {
    flex: 1; min-width: 100px;
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 12px; padding: 14px 16px; text-align: center;
}
.tax-pill-label { font-size: 0.7rem; color: rgba(255,255,255,0.6); font-weight: 600; letter-spacing: 1px; }
.tax-pill-value { font-size: 1.5rem; font-weight: 800; margin-top: 4px; }
.pill-igst  { color: #3B82F6; }
.pill-cgst  { color: #F59E0B; }
.pill-sgst  { color: #00B67A; }
.pill-nil   { color: #6EE7B7; }

/* ─── DETAIL ROWS ─── */
.detail-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 20px; }
.detail-item {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px; padding: 14px 16px;
}
.detail-item-label { font-size: 0.65rem; color: rgba(255,255,255,0.5); font-weight: 600; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 4px; }
.detail-item-value { font-size: 0.9rem; color: #FFFFFF; font-weight: 600; font-family: 'JetBrains Mono', monospace; }

/* ─── LOCATION TYPE CARD ─── */
.location-result {
    background: linear-gradient(135deg, rgba(59,130,246,0.15), rgba(29,78,216,0.08));
    border: 1px solid rgba(59,130,246,0.3);
    border-radius: 16px; padding: 20px; margin-top: 16px;
}
.location-result-igst {
    background: linear-gradient(135deg, rgba(59,130,246,0.15), rgba(29,78,216,0.08));
    border: 1px solid rgba(59,130,246,0.3);
}
.location-result-cgst {
    background: linear-gradient(135deg, rgba(245,158,11,0.15), rgba(217,119,6,0.08));
    border: 1px solid rgba(245,158,11,0.3);
}
.location-result-utgst {
    background: linear-gradient(135deg, rgba(139,92,246,0.15), rgba(109,40,217,0.08));
    border: 1px solid rgba(139,92,246,0.3);
}

/* ─── STAT MINI ─── */
.mini-stat {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 14px; padding: 18px 16px; text-align: center;
}
.mini-stat-num { font-size: 1.8rem; font-weight: 800; font-family: 'JetBrains Mono', monospace; }
.mini-stat-label { font-size: 0.7rem; color: rgba(255,255,255,0.55); font-weight: 600; letter-spacing: 1px; margin-top: 4px; }

/* ─── SEARCH INPUT OVERRIDE ─── */
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.08) !important;
    border: 1.5px solid rgba(255,255,255,0.15) !important;
    border-radius: 12px !important;
    color: white !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 1.1rem !important;
    padding: 14px 18px !important;
    transition: all 0.3s !important;
}
.stTextInput > div > div > input:focus {
    border-color: rgba(192,20,60,0.7) !important;
    background: rgba(255,255,255,0.12) !important;
    box-shadow: 0 0 0 3px rgba(192,20,60,0.2) !important;
}
.stTextInput > div > div > input::placeholder { color: rgba(255,255,255,0.35) !important; }
.stSelectbox > div > div {
    background: rgba(255,255,255,0.08) !important;
    border: 1.5px solid rgba(255,255,255,0.15) !important;
    border-radius: 12px !important;
    color: white !important;
}
.stSelectbox [data-baseweb="select"] span { color: white !important; }
.stSelectbox svg { fill: white !important; }

label { color: rgba(255,255,255,0.8) !important; font-weight: 600 !important; font-size: 0.8rem !important; letter-spacing: 0.5px !important; }

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #C0143C, #8B0F2C) !important;
    color: white !important; border: none !important;
    border-radius: 12px !important; padding: 12px 32px !important;
    font-weight: 700 !important; font-size: 0.95rem !important;
    font-family: 'Sora', sans-serif !important;
    box-shadow: 0 6px 20px rgba(192,20,60,0.4) !important;
    transition: all 0.3s !important; letter-spacing: 0.5px !important;
    width: 100% !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 28px rgba(192,20,60,0.55) !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.05) !important;
    border-radius: 14px !important; padding: 4px !important; gap: 4px !important;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 10px !important; color: rgba(255,255,255,0.6) !important;
    font-weight: 600 !important; font-family: 'Sora', sans-serif !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #C0143C, #8B0F2C) !important;
    color: white !important;
}

/* Divider */
hr { border-color: rgba(255,255,255,0.08) !important; }

/* Info / success / warning boxes */
.stAlert { border-radius: 12px !important; }

/* Scrollbar */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: rgba(255,255,255,0.04); }
::-webkit-scrollbar-thumb { background: rgba(192,20,60,0.5); border-radius: 10px; }

/* Table */
.stDataFrame { border-radius: 12px !important; overflow: hidden !important; }
</style>
""", unsafe_allow_html=True)


# ─── Load Data ───────────────────────────────────────────────────────────────
@st.cache_data
def load_hsn_data():
    df = pd.read_excel("HSN_SAC_GST_Rates.xlsx", sheet_name="All HSN & SAC Codes", dtype=str)
    df.columns = ['SNo','Code','Description','Type','GST_Total','CGST','SGST','IGST','Tax_Head','Schedule','Chapter']
    df['Code'] = df['Code'].astype(str).str.strip()
    return df

@st.cache_data
def load_gst_scenarios():
    df = pd.read_excel("GST_Complete_Dataset (2).xlsx", sheet_name="GST Dataset")
    return df

@st.cache_data
def load_rate_breakup():
    df = pd.read_excel("GST_Complete_Dataset (2).xlsx", sheet_name="Tax Calculator")
    return df

@st.cache_data
def load_logo_b64():
    with open("logo.png", "rb") as f:
        return base64.b64encode(f.read()).decode()

hsn_df     = load_hsn_data()
scenario_df = load_gst_scenarios()
logo_b64   = load_logo_b64()

# ─── State lists ─────────────────────────────────────────────────────────────
STATES = [
    "Andhra Pradesh","Arunachal Pradesh","Assam","Bihar","Chhattisgarh",
    "Goa","Gujarat","Haryana","Himachal Pradesh","Jharkhand","Karnataka",
    "Kerala","Madhya Pradesh","Maharashtra","Manipur","Meghalaya","Mizoram",
    "Nagaland","Odisha","Punjab","Rajasthan","Sikkim","Tamil Nadu",
    "Telangana","Tripura","Uttar Pradesh","Uttarakhand","West Bengal",
    "Delhi (NCT)","Jammu & Kashmir","Ladakh"
]
UTS = [
    "Chandigarh","Dadra & Nagar Haveli and Daman & Diu",
    "Lakshadweep","Puducherry","Andaman & Nicobar Islands"
]
SPECIAL = ["Export (Outside India)","Import (Into India)","SEZ Supply"]

ALL_LOCATIONS = STATES + UTS + SPECIAL

UT_NAMES = set(UTS)
EXPORT_NAMES = {"Export (Outside India)"}
IMPORT_NAMES = {"Import (Into India)"}
SEZ_NAMES = {"SEZ Supply"}

def classify_location(supplier, recipient):
    if supplier in EXPORT_NAMES or recipient in EXPORT_NAMES:
        return "ZERO_RATED"
    if supplier in IMPORT_NAMES or recipient in IMPORT_NAMES:
        return "IGST_IMPORT"
    if supplier in SEZ_NAMES or recipient in SEZ_NAMES:
        return "IGST"
    sup_ut = supplier in UT_NAMES
    rec_ut = recipient in UT_NAMES
    if supplier == recipient:
        if sup_ut:
            return "CGST_UTGST"
        return "CGST_SGST"
    return "IGST"

def get_tax_type_label(tx_type):
    mapping = {
        "IGST": ("IGST", "Inter-State Supply", "#3B82F6"),
        "CGST_SGST": ("CGST + SGST", "Intra-State Supply", "#F59E0B"),
        "CGST_UTGST": ("CGST + UTGST", "Intra-UT Supply", "#8B5CF6"),
        "ZERO_RATED": ("IGST @ 0%", "Zero-Rated (Export)", "#00B67A"),
        "IGST_IMPORT": ("IGST (Import)", "Import Supply", "#EF4444"),
    }
    return mapping.get(tx_type, ("IGST", "Inter-State", "#3B82F6"))

def rate_color_class(rate_str):
    if "NIL" in str(rate_str).upper() or "EXEMPT" in str(rate_str).upper():
        return "gst-rate-nil"
    try:
        r = float(str(rate_str).replace("%","").strip())
        if r <= 5:   return "gst-rate-low"
        if r <= 12:  return "gst-rate-mid"
        return "gst-rate-high"
    except:
        return "gst-rate-mid"


# ─── HEADER ──────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="portal-header">
    <img src="data:image/png;base64,{logo_b64}" style="height:72px; filter:drop-shadow(0 4px 12px rgba(0,0,0,0.4)); border-radius:8px;">
    <div class="portal-title">
        <h1>GST Intelligence Portal</h1>
        <p>India's Complete HSN/SAC Code Lookup &amp; GST Rate Intelligence Platform — 13,172 Codes, Real-time Tax Classification</p>
    </div>
    <div style="display:flex;flex-direction:column;gap:8px;align-items:flex-end">
        <div class="header-badge">🇮🇳 56th GST Council</div>
        <div class="header-badge">📋 GST 2.0 — Sep 2025</div>
        <div class="header-badge">✅ CBIC Verified</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── STATS ROW ───────────────────────────────────────────────────────────────
c1, c2, c3, c4, c5 = st.columns(5)
stats = [
    ("13,172", "Total Codes", "#C0143C"),
    ("12,604", "HSN Codes", "#3B82F6"),
    ("568", "SAC Codes", "#00B67A"),
    ("6", "GST Rate Slabs", "#F59E0B"),
    ("5", "Tax Heads", "#8B5CF6"),
]
for col, (num, label, color) in zip([c1,c2,c3,c4,c5], stats):
    with col:
        st.markdown(f"""
        <div class="mini-stat">
            <div class="mini-stat-num" style="color:{color}">{num}</div>
            <div class="mini-stat-label">{label}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── MAIN TABS ───────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "🔍  HSN/SAC Code Lookup",
    "📍  Location-Based GST",
    "📊  Rate Explorer",
    "📋  Transaction Scenarios"
])


# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — HSN/SAC LOOKUP
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown("<br>", unsafe_allow_html=True)
    lc, rc = st.columns([1, 1.6], gap="large")

    with lc:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-label">🔍 CODE LOOKUP</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Search HSN / SAC Code</div>', unsafe_allow_html=True)

        hsn_input = st.text_input("Enter HSN or SAC Code", placeholder="e.g. 10011010, 995411, 8517...", key="hsn_inp", label_visibility="visible")
        code_type = st.selectbox("Filter by Type", ["All", "HSN (Goods)", "SAC (Services)"], key="ctype")

        search_btn = st.button("🔍  Look Up GST Rate", key="lookup_btn")

        st.markdown("---")
        st.markdown('<div class="section-label">💡 QUICK EXAMPLES</div>', unsafe_allow_html=True)
        ex_codes = ["10011010", "85171200", "995411", "61091000", "30049099"]
        cols_ex = st.columns(len(ex_codes))
        for i, code in enumerate(ex_codes):
            if cols_ex[i].button(code, key=f"ex_{code}"):
                hsn_input = code
                search_btn = True
        st.markdown('</div>', unsafe_allow_html=True)

    with rc:
        results = pd.DataFrame()
        query = hsn_input.strip() if hsn_input else ""

        if query and (search_btn or query):
            # Filter
            filtered = hsn_df.copy()
            if code_type == "HSN (Goods)":
                filtered = filtered[filtered['Type'] == 'HSN']
            elif code_type == "SAC (Services)":
                filtered = filtered[filtered['Type'] == 'SAC']

            # Exact match first
            exact = filtered[filtered['Code'] == query]
            if len(exact) == 0:
                exact = filtered[filtered['Code'].str.startswith(query)]
            results = exact.head(10)

        if not results.empty:
            row = results.iloc[0]
            rate_str = str(row['GST_Total'])
            rate_class = rate_color_class(rate_str)

            # Determine display values
            cgst_v = str(row['CGST'])
            sgst_v = str(row['SGST'])
            igst_v = str(row['IGST'])
            tax_head = str(row['Tax_Head'])
            sched    = str(row['Schedule'])
            rtype    = str(row['Type'])
            desc     = str(row['Description'])
            chapter  = str(row['Chapter'])

            # Pill HTML
            if "NIL" in rate_str.upper() or "EXEMPT" in rate_str.upper():
                pills = f"""
                <div class="tax-breakdown-row">
                    <div class="tax-pill"><div class="tax-pill-label">GST RATE</div><div class="tax-pill-value pill-nil">NIL</div></div>
                    <div class="tax-pill"><div class="tax-pill-label">STATUS</div><div class="tax-pill-value pill-nil" style="font-size:1rem;">EXEMPT</div></div>
                </div>"""
            else:
                pills = f"""
                <div class="tax-breakdown-row">
                    <div class="tax-pill"><div class="tax-pill-label">IGST (Inter-State)</div><div class="tax-pill-value pill-igst">{igst_v}</div></div>
                    <div class="tax-pill"><div class="tax-pill-label">CGST (½ rate)</div><div class="tax-pill-value pill-cgst">{cgst_v}</div></div>
                    <div class="tax-pill"><div class="tax-pill-label">SGST/UTGST (½ rate)</div><div class="tax-pill-value pill-sgst">{sgst_v}</div></div>
                </div>"""

            st.markdown(f"""
            <div class="result-hero">
                <div style="display:flex;align-items:center;gap:20px;margin-bottom:24px;">
                    <div class="gst-rate-circle {rate_class}">
                        <div class="rate-number">{rate_str.replace(' / EXEMPT','').replace('NIL','0%')}</div>
                        <div class="rate-label">GST Rate</div>
                    </div>
                    <div style="flex:1">
                        <div style="font-size:0.65rem;color:rgba(255,255,255,0.5);font-weight:700;letter-spacing:2px;text-transform:uppercase;margin-bottom:6px">{rtype} CODE</div>
                        <div style="font-size:1.6rem;font-weight:800;color:#fff;font-family:'JetBrains Mono',monospace;">{row['Code']}</div>
                        <div style="font-size:0.85rem;color:rgba(255,255,255,0.75);margin-top:6px;line-height:1.4">{desc[:100]}{'...' if len(desc)>100 else ''}</div>
                    </div>
                </div>
                {pills}
                <div class="detail-grid">
                    <div class="detail-item"><div class="detail-item-label">Tax Head</div><div class="detail-item-value">{tax_head}</div></div>
                    <div class="detail-item"><div class="detail-item-label">GST Schedule</div><div class="detail-item-value">{sched}</div></div>
                    <div class="detail-item"><div class="detail-item-label">Code Type</div><div class="detail-item-value">{rtype}</div></div>
                    <div class="detail-item"><div class="detail-item-label">Chapter</div><div class="detail-item-value" style="font-size:0.75rem">{chapter[:50]}{'...' if len(chapter)>50 else ''}</div></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if len(results) > 1:
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.markdown(f'<div class="section-label">📋 {len(results)} MATCHING CODES</div>', unsafe_allow_html=True)
                show_df = results[['Code','Description','Type','GST_Total','CGST','SGST','IGST','Tax_Head']].copy()
                show_df.columns = ['Code','Description','Type','GST %','CGST %','SGST %','IGST %','Tax Head']
                st.dataframe(show_df, use_container_width=True, height=250)
                st.markdown('</div>', unsafe_allow_html=True)
        elif query and search_btn:
            st.markdown(f"""
            <div class="glass-card" style="text-align:center;padding:48px;">
                <div style="font-size:3rem;margin-bottom:12px;">🔎</div>
                <div style="color:#fff;font-size:1.1rem;font-weight:700;">No results for "{query}"</div>
                <div style="color:rgba(255,255,255,0.5);margin-top:8px;font-size:0.85rem;">Try a shorter prefix or check the code format</div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="glass-card" style="text-align:center;padding:60px 40px;">
                <div style="font-size:4rem;margin-bottom:16px;">🏷️</div>
                <div style="color:#fff;font-size:1.2rem;font-weight:700;margin-bottom:8px;">Enter an HSN or SAC Code</div>
                <div style="color:rgba(255,255,255,0.5);font-size:0.9rem;line-height:1.6">
                    Search by full code or prefix<br>
                    Covers 12,604 HSN (goods) + 568 SAC (services) codes
                </div>
            </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — LOCATION-BASED GST
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("<br>", unsafe_allow_html=True)
    lc2, rc2 = st.columns([1, 1.5], gap="large")

    with lc2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-label">📍 LOCATION CLASSIFIER</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Determine IGST vs CGST+SGST</div>', unsafe_allow_html=True)

        supplier_loc  = st.selectbox("Supplier / Service Provider Location", ALL_LOCATIONS, key="sup_loc")
        recipient_loc = st.selectbox("Recipient / Place of Supply", ALL_LOCATIONS, key="rec_loc")
        hsn_for_loc   = st.text_input("HSN/SAC Code (optional, for rate)", placeholder="e.g. 85171200", key="hsn_loc")
        loc_btn       = st.button("📍  Classify GST Type", key="loc_btn")
        st.markdown('</div>', unsafe_allow_html=True)

    with rc2:
        if loc_btn or (supplier_loc and recipient_loc):
            tx_type = classify_location(supplier_loc, recipient_loc)
            label, sublabel, color = get_tax_type_label(tx_type)

            # Optional HSN rate
            rate_info = ""
            if hsn_for_loc.strip():
                hcode = hsn_for_loc.strip()
                hrow = hsn_df[hsn_df['Code'] == hcode]
                if len(hrow) == 0:
                    hrow = hsn_df[hsn_df['Code'].str.startswith(hcode)]
                if not hrow.empty:
                    hr = hrow.iloc[0]
                    total_gst = str(hr['GST_Total'])
                    if tx_type == "IGST" or tx_type == "IGST_IMPORT":
                        tax_split = f"IGST: {hr['IGST']}"
                    elif tx_type == "ZERO_RATED":
                        tax_split = "IGST @ 0% (Zero-Rated)"
                    elif tx_type in ("CGST_SGST", "CGST_UTGST"):
                        utgst_label = "UTGST" if tx_type == "CGST_UTGST" else "SGST"
                        tax_split = f"CGST: {hr['CGST']} + {utgst_label}: {hr['SGST']}"
                    else:
                        tax_split = total_gst

                    rate_class2 = rate_color_class(total_gst)
                    rate_info = f"""
                    <div style="margin-top:20px;background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.12);border-radius:14px;padding:18px;display:flex;align-items:center;gap:20px;">
                        <div class="gst-rate-circle {rate_class2}" style="width:80px;height:80px;flex-shrink:0;">
                            <div style="font-size:1.4rem;font-weight:800;color:white;">{total_gst.replace(' / EXEMPT','')}</div>
                            <div style="font-size:0.65rem;color:rgba(255,255,255,0.8)">Total GST</div>
                        </div>
                        <div>
                            <div style="font-size:0.65rem;color:rgba(255,255,255,0.5);letter-spacing:1.5px;text-transform:uppercase;margin-bottom:4px">HSN {hr['Code']} — Tax Split</div>
                            <div style="font-size:1.1rem;font-weight:700;color:#fff;">{tax_split}</div>
                            <div style="font-size:0.75rem;color:rgba(255,255,255,0.55);margin-top:4px">{str(hr['Description'])[:80]}</div>
                        </div>
                    </div>"""

            # Explanation text
            explanations = {
                "IGST": f"Since <b>{supplier_loc}</b> and <b>{recipient_loc}</b> are different states/territories, this is an <b>inter-state supply</b>. IGST applies at the full GST rate and flows to the Central Government.",
                "CGST_SGST": f"Since supplier and recipient are both in <b>{supplier_loc}</b>, this is an <b>intra-state supply</b>. The total GST rate is split equally — half as CGST (Central) and half as SGST (State).",
                "CGST_UTGST": f"Both locations are in the Union Territory of <b>{supplier_loc}</b>. UTGST replaces SGST for Union Territories without a legislature. Split equally with CGST.",
                "ZERO_RATED": "Exports are <b>zero-rated supplies</b> under GST. IGST is charged at 0%. The exporter can claim a refund of input tax credit or supply under a Letter of Undertaking (LUT).",
                "IGST_IMPORT": "Imports are treated as <b>inter-state supplies</b> and IGST is levied at the point of customs clearance (port of entry) on the assessable value including Basic Customs Duty."
            }
            expl = explanations.get(tx_type, "")

            # Arrow direction icons
            same = supplier_loc == recipient_loc
            arrow_icon = "↔️" if same else "➡️"

            st.markdown(f"""
            <div class="result-hero">
                <div style="display:flex;align-items:center;gap:16px;margin-bottom:24px;">
                    <div style="width:20px;height:70px;border-radius:4px;background:{color};flex-shrink:0;"></div>
                    <div>
                        <div style="font-size:0.65rem;color:rgba(255,255,255,0.5);letter-spacing:2px;text-transform:uppercase;margin-bottom:4px">Tax Classification</div>
                        <div style="font-size:2rem;font-weight:800;color:#fff;">{label}</div>
                        <div style="font-size:0.85rem;color:rgba(255,255,255,0.65);margin-top:4px">{sublabel}</div>
                    </div>
                </div>
                <div style="display:flex;align-items:center;gap:12px;background:rgba(255,255,255,0.05);border-radius:12px;padding:14px 18px;margin-bottom:16px;">
                    <div style="flex:1;text-align:center;">
                        <div style="font-size:0.65rem;color:rgba(255,255,255,0.45);letter-spacing:1px;text-transform:uppercase">SUPPLIER / FROM</div>
                        <div style="font-size:0.9rem;font-weight:700;color:#fff;margin-top:4px">{supplier_loc}</div>
                    </div>
                    <div style="font-size:1.6rem">{arrow_icon}</div>
                    <div style="flex:1;text-align:center;">
                        <div style="font-size:0.65rem;color:rgba(255,255,255,0.45);letter-spacing:1px;text-transform:uppercase">RECIPIENT / TO</div>
                        <div style="font-size:0.9rem;font-weight:700;color:#fff;margin-top:4px">{recipient_loc}</div>
                    </div>
                </div>
                <div style="background:rgba(255,255,255,0.05);border-left:3px solid {color};border-radius:0 10px 10px 0;padding:14px 16px;font-size:0.85rem;color:rgba(255,255,255,0.75);line-height:1.6">
                    {expl}
                </div>
                {rate_info}
            </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — RATE EXPLORER (charts)
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("<br>", unsafe_allow_html=True)

    # Rate distribution
    rate_counts = hsn_df['GST_Total'].value_counts().reset_index()
    rate_counts.columns = ['Rate','Count']
    order = ['NIL / EXEMPT','3%','5%','12%','18%','28%']
    rate_counts['Rate'] = pd.Categorical(rate_counts['Rate'], categories=order, ordered=True)
    rate_counts = rate_counts.sort_values('Rate')

    colors_bar = ['#00B67A','#8B5CF6','#3B82F6','#F59E0B','#C0143C','#7C3AED']

    fig_bar = go.Figure(go.Bar(
        x=rate_counts['Rate'], y=rate_counts['Count'],
        marker=dict(color=colors_bar[:len(rate_counts)],
                    line=dict(width=0)),
        text=rate_counts['Count'], textposition='outside',
        textfont=dict(color='white', family='JetBrains Mono', size=13)
    ))
    fig_bar.update_layout(
        title=dict(text="HSN/SAC Codes by GST Rate Slab", font=dict(color='white', size=16, family='Sora')),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='rgba(255,255,255,0.7)', family='Sora'),
        xaxis=dict(gridcolor='rgba(255,255,255,0.06)', tickfont=dict(color='white')),
        yaxis=dict(gridcolor='rgba(255,255,255,0.06)', tickfont=dict(color='rgba(255,255,255,0.6)')),
        margin=dict(t=50, b=20, l=20, r=20), height=340
    )

    # HSN vs SAC donut
    type_counts = hsn_df['Type'].value_counts()
    fig_donut = go.Figure(go.Pie(
        labels=type_counts.index, values=type_counts.values,
        hole=0.65,
        marker=dict(colors=['#C0143C','#3B82F6']),
        textfont=dict(color='white', family='Sora'),
    ))
    fig_donut.update_layout(
        title=dict(text="HSN vs SAC Distribution", font=dict(color='white', size=16, family='Sora')),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='rgba(255,255,255,0.7)', family='Sora'),
        legend=dict(font=dict(color='white')),
        margin=dict(t=50, b=20, l=10, r=10), height=340
    )

    c_chart1, c_chart2 = st.columns([1.7, 1], gap="large")
    with c_chart1:
        st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})
    with c_chart2:
        st.plotly_chart(fig_donut, use_container_width=True, config={'displayModeBar': False})

    # Tax Head breakdown
    head_counts = hsn_df['Tax_Head'].value_counts().reset_index()
    head_counts.columns = ['Head','Count']
    fig_head = go.Figure(go.Bar(
        y=head_counts['Head'], x=head_counts['Count'],
        orientation='h',
        marker=dict(color=['#C0143C','#3B82F6','#8B5CF6'][:len(head_counts)]),
        text=head_counts['Count'], textposition='auto',
        textfont=dict(color='white', family='JetBrains Mono')
    ))
    fig_head.update_layout(
        title=dict(text="Codes by Tax Head", font=dict(color='white', size=16, family='Sora')),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='rgba(255,255,255,0.7)', family='Sora'),
        xaxis=dict(gridcolor='rgba(255,255,255,0.06)', tickfont=dict(color='rgba(255,255,255,0.6)')),
        yaxis=dict(tickfont=dict(color='white', size=11)),
        margin=dict(t=50, b=20, l=10, r=20), height=220
    )
    st.plotly_chart(fig_head, use_container_width=True, config={'displayModeBar': False})

    # Searchable table
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">📋 BROWSE ALL CODES</div>', unsafe_allow_html=True)
    f_col1, f_col2, f_col3 = st.columns(3)
    with f_col1:
        f_rate = st.selectbox("Filter by GST Rate", ["All"] + list(hsn_df['GST_Total'].unique()), key="f_rate")
    with f_col2:
        f_type = st.selectbox("Filter by Type", ["All","HSN","SAC"], key="f_type2")
    with f_col3:
        f_search = st.text_input("Search description", placeholder="e.g. mobile, wheat, software", key="f_search")

    browse_df = hsn_df.copy()
    if f_rate != "All":
        browse_df = browse_df[browse_df['GST_Total'] == f_rate]
    if f_type != "All":
        browse_df = browse_df[browse_df['Type'] == f_type]
    if f_search:
        browse_df = browse_df[browse_df['Description'].str.contains(f_search, case=False, na=False)]

    show_browse = browse_df[['Code','Description','Type','GST_Total','CGST','SGST','IGST','Tax_Head']].head(100)
    show_browse.columns = ['Code','Description','Type','GST %','CGST %','SGST %','IGST %','Tax Head']
    st.dataframe(show_browse, use_container_width=True, height=350)
    st.caption(f"Showing {len(show_browse)} of {len(browse_df):,} matching codes")
    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — TRANSACTION SCENARIOS
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-label">📋 50 REAL-WORLD GST TRANSACTION SCENARIOS</div>', unsafe_allow_html=True)

    search_scenario = st.text_input("🔍 Search scenarios", placeholder="e.g. export, hotel, e-commerce, import...", key="sc_search")

    sc_df = scenario_df.copy()
    if search_scenario:
        mask = (
            sc_df['Transaction Scenario'].str.contains(search_scenario, case=False, na=False) |
            sc_df['Supplier Location'].str.contains(search_scenario, case=False, na=False) |
            sc_df['Tax Applicable'].str.contains(search_scenario, case=False, na=False)
        )
        sc_df = sc_df[mask]

    for _, row in sc_df.iterrows():
        tax = str(row['Tax Applicable'])
        if "IGST" in tax and "Zero" in tax:
            badge_color = "#00B67A"; badge_bg = "rgba(0,182,122,0.12)"
        elif "IGST" in tax:
            badge_color = "#3B82F6"; badge_bg = "rgba(59,130,246,0.12)"
        elif "UTGST" in tax:
            badge_color = "#8B5CF6"; badge_bg = "rgba(139,92,246,0.12)"
        else:
            badge_color = "#F59E0B"; badge_bg = "rgba(245,158,11,0.12)"

        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);border-radius:14px;padding:16px 20px;margin-bottom:10px;display:flex;gap:16px;align-items:flex-start;">
            <div style="font-size:1rem;font-weight:800;color:rgba(255,255,255,0.2);font-family:'JetBrains Mono',monospace;min-width:30px">#{row['#']}</div>
            <div style="flex:1">
                <div style="font-size:0.9rem;color:#fff;font-weight:600;margin-bottom:8px;">{row['Transaction Scenario']}</div>
                <div style="display:flex;gap:10px;flex-wrap:wrap;">
                    <span style="background:rgba(255,255,255,0.06);border-radius:6px;padding:3px 10px;font-size:0.72rem;color:rgba(255,255,255,0.6)">📍 {row['Supplier Location']} → {row['Place of Supply']}</span>
                    <span style="background:{badge_bg};border:1px solid {badge_color}30;border-radius:6px;padding:3px 10px;font-size:0.72rem;color:{badge_color};font-weight:700">{tax}</span>
                    <span style="background:rgba(255,255,255,0.04);border-radius:6px;padding:3px 10px;font-size:0.72rem;color:rgba(255,255,255,0.5)">{row['Tax Split']}</span>
                </div>
                <div style="margin-top:6px;font-size:0.75rem;color:rgba(255,255,255,0.35);font-style:italic">{row['Rule / Reason']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    if sc_df.empty:
        st.markdown("""<div class="glass-card" style="text-align:center;padding:48px">
            <div style="font-size:3rem">🔍</div>
            <div style="color:white;font-size:1.1rem;font-weight:700;margin-top:12px">No scenarios matched</div>
        </div>""", unsafe_allow_html=True)

# ─── Footer ──────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:32px 0 16px;color:rgba(255,255,255,0.3);font-size:0.75rem;letter-spacing:0.5px">
    Data Source: CBIC / GST Portal, India &nbsp;|&nbsp; GST 2.0 — 56th GST Council (Sep 2025) &nbsp;|&nbsp; 13,172 HSN/SAC Codes
</div>
""", unsafe_allow_html=True)
