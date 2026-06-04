import streamlit as st
import pandas as pd
import plotly.express as px

# Streamlit page configuration
st.set_page_config(page_title="EHR Data Quality Analyzer", layout="wide")

st.title("🏥 EHR Data Quality & Clinical Analyzer")
st.markdown("This application evaluates data integrity and clinical consistency within Electronic Health Records (EHR).")

# 1. Data ingestion pipeline
@st.cache_data
def load_data():
    df = pd.read_csv("mock_ehr.csv")
    df['last_visit'] = pd.to_datetime(df['last_visit'])
    return df

df = load_data()

# 2. Key Performance Indicators (KPIs) / Quality Gates
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Records", len(df))
with col2:
    missing_bps = df['systolic_bp'].isna().sum()
    st.metric("Missing Critical Data (Systolic BP)", missing_bps, delta=f"{missing_bps} missing", delta_color="inverse")
with col3:
    # Clinical logic: extreme physiological outliers or biological impossibilities
    clinical_alerts = df[(df['age'] > 115) | (df['systolic_bp'] > 250)].shape[0]
    st.metric("Clinical Inconsistency Alerts", clinical_alerts, delta=f"{clinical_alerts} anomalies", delta_color="inverse")

st.divider()

# 3. Data Quality Audit Section (Highly valued by technical recruiters)
st.header("🔍 Data Quality Audit Report")

tab1, tab2 = st.tabs(["📋 Raw Dataset", "⚠️ Detected Clinical Anomalies"])

with tab1:
    st.write("EHR Dataset Preview:")
    st.dataframe(df, use_container_width=True)

with tab2:
    st.subheader("Records Outside Biological Ranges / Input Errors")
    
    # Data quality flag assignment logic
    alerts = []
    
    for idx, row in df.iterrows():
        if row['age'] > 115:
            alerts.append({
                "Patient ID": row['patient_id'], 
                "Field": "Age", 
                "Value": row['age'], 
                "Issue": "Extreme age outlier (>115 years). Highly probable data entry typo."
            })
        if pd.isna(row['systolic_bp']):
            alerts.append({
                "Patient ID": row['patient_id'], 
                "Field": "Systolic BP", 
                "Value": "N/A", 
                "Issue": "Missing critical physiological variable required for chronic disease tracking."
            })
        elif row['systolic_bp'] > 250:
            alerts.append({
                "Patient ID": row['patient_id'], 
                "Field": "Systolic BP", 
                "Value": row['systolic_bp'], 
                "Issue": "Systolic BP > 250 mmHg. Physiologically implausible under normal conditions; suspect sensor malfunction."
            })
            
    if alerts:
        alerts_df = pd.DataFrame(alerts)
        st.table(alerts_df)
    else:
        st.success("Data validation passed. No clinical anomalies detected.")

st.divider()

# 4. Clinical Insights and Population Health Analytics
st.header("📈 Population Health Analytics")

col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("Diagnosis Distribution")
    fig_pie = px.pie(df, names='diagnosis', title='Prevalence of Clinical Conditions', hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig_pie, use_container_width=True)

with col_chart2:
    st.subheader("Biomarker Analysis: HbA1c vs Age")
    # Exclude extreme biological outliers for clean data presentation
    clean_df = df[df['age'] <= 115]
    fig_scatter = px.scatter(clean_df, x='age', y='hba1c', color='diagnosis', size='age', hover_data=['name'], title='HbA1c Levels by Age (Filtered Dataset)')
    st.plotly_chart(fig_scatter, use_container_width=True)
    