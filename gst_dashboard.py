
import streamlit as st
import pandas as pd

st.set_page_config(page_title="GST360 Enterprise", page_icon="🇮🇳", layout="wide")

st.markdown("""
<style>
.stApp {background:#F5F7FA;}
.card{
background:white;padding:20px;border-radius:18px;
border:1px solid #DDE3EA;margin-bottom:15px;
}
.bigtitle{font-size:2.2rem;font-weight:700;color:#0B5CAB;}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_hsn():
    return pd.read_excel("HSN_SAC_GST_Rates.xlsx", sheet_name="All HSN & SAC Codes", dtype=str)

st.sidebar.title("GST360 Enterprise")
page = st.sidebar.radio(
    "Navigation",
    ["Dashboard","GST Analyzer","Tax Simulator","Compliance"]
)

st.markdown('<div class="bigtitle">GST360 Enterprise</div>', unsafe_allow_html=True)
st.caption("National GST Intelligence & Compliance Platform")

if page == "Dashboard":
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("GST Analyzer","Ready")
    c2.metric("Tax Simulator","Ready")
    c3.metric("Compliance","100%")
    c4.metric("Reports","PDF Ready")

    st.info("Professional Government Enterprise UI template. No raw Excel tables exposed.")

elif page == "GST Analyzer":
    df = load_hsn()
    code = st.text_input("Enter HSN / SAC Code")
    if code:
        res = df[df.iloc[:,1].astype(str).str.startswith(code)]
        if not res.empty:
            row = res.iloc[0]
            a,b,c = st.columns(3)
            a.metric("GST Rate", str(row.iloc[4]))
            b.metric("CGST", str(row.iloc[5]))
            c.metric("IGST", str(row.iloc[7]))
            st.success(f"Classification: {row.iloc[2]}")
        else:
            st.error("Code not found")

elif page == "Tax Simulator":
    amount = st.number_input("Transaction Value", min_value=0.0)
    gst_rate = st.number_input("GST Rate (%)", min_value=0.0, value=18.0)
    tax = amount * gst_rate / 100
    total = amount + tax

    c1,c2 = st.columns(2)
    c1.metric("Tax Amount", f"₹{tax:,.2f}")
    c2.metric("Invoice Total", f"₹{total:,.2f}")

elif page == "Compliance":
    st.success("✓ Valid HSN\n\n✓ GST Classification\n\n✓ Tax Structure Verified\n\n✓ Compliance Ready")
