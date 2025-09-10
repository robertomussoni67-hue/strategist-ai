import streamlit as st
import json
from pathlib import Path

# === Carica ultimo report JSON ===
def load_latest_report():
    reports_dir = Path("reports")
    files = sorted(reports_dir.glob("strategist_report_*.json"), reverse=True)
    if not files:
        return None
    with open(files[0], "r", encoding="utf-8") as f:
        return json.load(f)

# === Layout ===
st.set_page_config(page_title="Strategist Dashboard", layout="wide")
st.title("📊 Strategist Dashboard")

data = load_latest_report()
if not data:
    st.warning("Nessun report trovato nella cartella 'reports'.")
    st.stop()

# === Profilo utente ===
st.sidebar.header("👤 Profilo utente")
st.sidebar.write(f"**Nome:** Roberto")
st.sidebar.write(f"**Età:** 45")
st.sidebar.write(f"**Profilo rischio:** {data.get('allocation_philosophy', 'N/A')}")
st.sidebar.write(f"**Orizzonte:** 10 anni")
st.sidebar.write(f"**Regime macro:** {data['macro'].get('regime', 'N/A')}")
st.sidebar.write(f"**Sentiment:** {data['sentiment'].get('market_sentiment', 'N/A')}")

# === Allocazione ===
st.subheader("📈 Allocazione strategica")
alloc = data.get("allocation", {})
st.bar_chart(alloc)

# === Piano allocativo ===
st.subheader("🧭 Piano allocativo")
plan = data.get("plan", [])
st.dataframe(plan)

# === Backtest ===
st.subheader("📉 Backtest storico")
backtest = data.get("backtest", {})
if backtest:
    st.metric("CAGR", f"{backtest.get('cagr', 0)}%")
    st.metric("Volatilità", f"{backtest.get('volatility', 0)}%")
    st.metric("Sharpe Ratio", backtest.get("sharpe_ratio", "N/A"))
    st.metric("Max Drawdown", f"{backtest.get('max_drawdown', 0)}%")

# === Rischio ===
st.subheader("🧠 Analisi del rischio")
risk = data.get("risk", {})
if risk:
    st.json(risk["metrics"])
    st.write("**Top posizioni:**")
    st.table(risk.get("top_positions", []))
    st.write("**Settori principali:**")
    st.table(risk.get("sectors", {}).get("top_sectors", []))