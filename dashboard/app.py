"""
Financial Inclusion Dashboard

Interactive dashboard for visualizing Ethiopia's financial inclusion forecasts
and analysis results.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Ethiopia Financial Inclusion Forecast",
    page_icon="📊",
    layout="wide"
)

# Title
st.title("🇪🇹 Ethiopia Financial Inclusion Forecast Dashboard")
st.markdown("*Tracking Ethiopia's Digital Financial Transformation*")

# Sidebar
st.sidebar.header("Navigation")
page = st.sidebar.selectbox("Select Page", [
    "Overview",
    "Access Metrics",
    "Usage Metrics", 
    "Event Impact Analysis",
    "Forecasts",
    "Methodology"
])

# Load data (placeholder for now)
@st.cache_data
def load_data():
    # Placeholder - will be replaced with actual data loading
    return pd.DataFrame()

# Main content based on selected page
if page == "Overview":
    st.header("Project Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Account Ownership (2024)", "49%", "+3pp since 2021")
        st.metric("Digital Payment Usage", "~35%", "Growing rapidly")
        
    with col2:
        st.metric("Telebirr Users", "54M+", "Since 2021")
        st.metric("M-Pesa Users", "10M+", "Since 2023")
    
    st.markdown("""
    ### Key Insights
    - Ethiopia is undergoing rapid digital financial transformation
    - Digital P2P transfers now surpass ATM withdrawals
    - Mobile money platforms driving inclusion growth
    - Policy interventions showing measurable impact
    """)

elif page == "Access Metrics":
    st.header("Access - Account Ownership")
    st.info("Account ownership metrics and trends will be displayed here")

elif page == "Usage Metrics":
    st.header("Usage - Digital Payment Adoption")
    st.info("Digital payment usage metrics will be displayed here")

elif page == "Event Impact Analysis":
    st.header("Event Impact Analysis")
    st.info("Analysis of policy and market event impacts will be displayed here")

elif page == "Forecasts":
    st.header("2025-2027 Forecasts")
    st.info("Forecast visualizations will be displayed here")

elif page == "Methodology":
    st.header("Methodology")
    st.markdown("""
    ### Data Sources
    - World Bank Global Findex Database
    - Mobile money operator reports
    - National Bank of Ethiopia data
    - Policy and event records
    
    ### Modeling Approach
    - Time series analysis with intervention variables
    - Event impact estimation using comparable country evidence
    - Regression modeling with policy indicators
    - Forecasting with confidence bounds
    """)

# Footer
st.markdown("---")
st.markdown("*Dashboard developed by Selam Analytics for Ethiopia Financial Inclusion Forecasting Project*")
