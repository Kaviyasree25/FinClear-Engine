import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.ensemble import IsolationForest
import time

# --- PAGE CONFIGURATION (Looks Professional) ---
st.set_page_config(page_title="FinNet | DTCC Settlement Engine", layout="wide", page_icon="🏦")

# --- CUSTOM CSS FOR "ENTERPRISE" FEEL ---
st.markdown("""
<style>
    .metric-box {
        background-color: #1e1e1e;
        border-left: 5px solid #4CAF50;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 10px;
    }
    .alert-box {
        background-color: #3b1e1e;
        border-left: 5px solid #FF5252;
        padding: 15px;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
col1, col2 = st.columns([1, 5])
with col1:
    st.write("## 🏦")
with col2:
    st.title("FinNet: Intelligent Post-Trade Settlement Engine")
    st.caption("Simulating T+1 Settlement • Multilateral Netting • AI Risk Detection")

st.divider()

# --- SIDEBAR CONTROLS ---
st.sidebar.header("🕹️ Simulation Control")
sim_speed = st.sidebar.slider("Transaction Speed (TPS)", 100, 5000, 1000)
risk_threshold = st.sidebar.slider("AI Risk Sensitivity", 0.01, 0.1, 0.05)

# --- CLASS 1: THE DATA GENERATOR (Simulating the Market) ---
class MarketSimulator:
    def generate_trades(self, n=500):
        # Create realistic fake data
        data = {
            'Trade_ID': [f"TRX-{np.random.randint(10000, 99999)}" for _ in range(n)],
            'Buyer': np.random.choice(['JPMorgan', 'Goldman Sachs', 'Morgan Stanley', 'Citi', 'BlackRock'], n),
            'Seller': np.random.choice(['JPMorgan', 'Goldman Sachs', 'Morgan Stanley', 'Citi', 'BlackRock'], n),
            'Symbol': np.random.choice(['AAPL', 'GOOGL', 'TSLA', 'MSFT', 'AMZN'], n),
            'Quantity': np.random.randint(10, 1000, n),
            'Price': np.random.uniform(100, 1500, n).round(2),
            'Timestamp': pd.date_range(start='2025-01-01', periods=n, freq='ms')
        }
        df = pd.DataFrame(data)
        # Calculate total value
        df['Total_Value'] = df['Quantity'] * df['Price']
        
        # Inject "Fraud" (Anomalies) for AI to find
        # Make a few trades largely huge to simulate a "Fat Finger" error
        df.loc[0:2, 'Total_Value'] = df.loc[0:2, 'Total_Value'] * 50 
        return df

# --- CLASS 2: THE AI RISK ENGINE (The "Advanced" Part) ---
class RiskEngine:
    def detect_anomalies(self, df):
        # Machine Learning: Isolation Forest (Anomaly Detection)
        model = IsolationForest(contamination=risk_threshold, random_state=42)
        # We look at Quantity and Total Value to find weird trades
        df['Anomaly_Score'] = model.fit_predict(df[['Quantity', 'Total_Value']])
        # -1 means Anomaly, 1 means Normal
        return df

# --- CLASS 3: THE NETTING ALGORITHM (The "DTCC" Logic) ---
class NettingEngine:
    def run_netting(self, df):
        # Filter only Valid trades (No Anomalies)
        valid_trades = df[df['Anomaly_Score'] == 1]
        
        # LOGIC: If JP buys $100 and sells $80, they only pay $20.
        # Group by Buyer to see what they OWE
        pay_obligations = valid_trades.groupby('Buyer')['Total_Value'].sum().reset_index()
        pay_obligations.columns = ['Entity', 'To_Pay']
        
        # Group by Seller to see what they RECEIVE
        receive_obligations = valid_trades.groupby('Seller')['Total_Value'].sum().reset_index()
        receive_obligations.columns = ['Entity', 'To_Receive']
        
        # Merge
        net_df = pd.merge(pay_obligations, receive_obligations, on='Entity', how='outer').fillna(0)
        
        # FINAL CALCULATION
        net_df['Net_Position'] = net_df['To_Receive'] - net_df['To_Pay']
        net_df['Status'] = net_df['Net_Position'].apply(lambda x: "PAY TO DTCC" if x < 0 else "RECEIVE FROM DTCC")
        
        # Efficiency Metric
        gross_volume = valid_trades['Total_Value'].sum()
        net_volume = abs(net_df['Net_Position']).sum() / 2 # Divided by 2 because pay/receive cancel out in system view
        savings = ((gross_volume - net_volume) / gross_volume) * 100
        
        return net_df, savings, gross_volume, net_volume

# --- RUNNING THE SYSTEM ---

# 1. Initialize
if 'df' not in st.session_state:
    simulator = MarketSimulator()
    st.session_state.df = simulator.generate_trades(1000)

# 2. Main Dashboard Layout
tab1, tab2, tab3 = st.tabs(["🚀 Real-Time Feed", "🧠 AI Risk Analysis", "📉 Netting & Settlement"])

with tab1:
    st.subheader("Live Market Ingestion (Kafka Stream Simulation)")
    st.dataframe(st.session_state.df.head(10), use_container_width=True)
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Transactions Processed", f"{len(st.session_state.df):,}")
    c2.metric("Total Market Volume", f"${st.session_state.df['Total_Value'].sum()/1e6:.2f} M")
    c3.metric("Active Counterparties", "5 (Major Banks)")

with tab2:
    st.subheader("🛡️ AI Fraud & Anomaly Detection")
    
    if st.button("Run AI Risk Scan"):
        risk_engine = RiskEngine()
        with st.spinner("Scanning transaction patterns..."):
            time.sleep(1) # Fake processing time
            analyzed_df = risk_engine.detect_anomalies(st.session_state.df)
            st.session_state.analyzed_df = analyzed_df
            
        anomalies = analyzed_df[analyzed_df['Anomaly_Score'] == -1]
        
        st.error(f"🚨 ALERT: {len(anomalies)} High-Risk Transactions Detected")
        st.dataframe(anomalies, use_container_width=True)
        
        # Chart
        fig = px.scatter(analyzed_df, x="Quantity", y="Total_Value", color="Anomaly_Score", 
                         title="AI Cluster Analysis (Red = Fraud)", color_continuous_scale=["red", "blue"])
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Click the button to run the Isolation Forest Algorithm.")

with tab3:
    st.subheader("💰 Multilateral Netting Engine (T+1 Optimization)")
    
    if 'analyzed_df' in st.session_state:
        netting_engine = NettingEngine()
        net_df, savings, gross, net = netting_engine.run_netting(st.session_state.analyzed_df)
        
        # Impact Metrics
        m1, m2, m3 = st.columns(3)
        m1.metric("Gross Obligation", f"${gross/1e6:.2f} M", help="Total money moving without Netting")
        m2.metric("Net Settlement", f"${net/1e6:.2f} M", help="Actual money moving WITH Netting")
        m3.metric("Liquidity Saved", f"{savings:.2f}%", delta="High Efficiency")
        
        st.divider()
        st.write("### Final Settlement Instructions")
        st.dataframe(net_df.style.format({"To_Pay": "${:,.2f}", "To_Receive": "${:,.2f}", "Net_Position": "${:,.2f}"}), use_container_width=True)
        
        # Visualization
        fig2 = go.Figure(data=[
            go.Bar(name='Pay Obligation', x=net_df['Entity'], y=net_df['To_Pay']),
            go.Bar(name='Receive Obligation', x=net_df['Entity'], y=net_df['To_Receive'])
        ])
        fig2.update_layout(barmode='group', title="Counterparty Obligations")
        st.plotly_chart(fig2, use_container_width=True)
        
    else:
        st.warning("Please run the AI Risk Scan first to filter out bad trades.")