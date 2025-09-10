import json
import streamlit as st
from pathlib import Path
import pandas as pd
import altair as alt

st.set_page_config(page_title="Strategist Dashboard v2", layout="wide")

# === Caricamento report disponibili ===
reports_folder = Path("reports")
report_files = sorted(reports_folder.glob("strategist_report_*.json"), key=lambda f: f.stat().st_mtime, reverse=True)

if not report_files:
    st.error("⚠️ Nessun report trovato nella cartella 'reports'. Esegui Strategist prima di aprire la dashboard.")
    st.stop()

# === Selettore report ===
selected_file = st.selectbox("📅 Seleziona un report", report_files, format_func=lambda f: f.name)

with open(selected_file, "r", encoding="utf-8") as f:
    data = json.load(f)

st.title("📊 Strategist Dashboard v2")
st.caption(f"Report selezionato: `{selected_file.name}`")

# === Regime macroeconomico ===
macro = data.get("macro", {})
st.subheader("🧠 Regime Macroeconomico")
col1, col2, col3 = st.columns(3)
col1.metric("Inflazione YoY", f"{macro.get('inflation_yoy', '?')}%")
col2.metric("Tasso di policy", f"{macro.get('policy_rate', '?')}%")
col3.metric("Crescita PIL", f"{macro.get('gdp_growth', '?')}%")
st.write("**Regime identificato:**", macro.get("regime", "N/A"))
with st.expander("📈 Outlook 3-6 mesi"):
    st.json(macro.get("outlook_3_6m", {}))

# === Sentiment ===
sentiment = data.get("sentiment", {})
st.subheader("💬 Sentiment di Mercato")
col1, col2 = st.columns(2)
col1.metric("Sentiment", sentiment.get("market_sentiment", "N/A"))
col2.metric("Confidenza", sentiment.get("confidence", "N/A"))
with st.expander("🔍 Dettagli sentiment"):
    st.json(sentiment.get("details", {}))

# === Titoli selezionati ===
stocks = data.get("stocks", [])
st.subheader("📈 Titoli Selezionati")
stocks_df = pd.DataFrame(stocks)
st.dataframe(stocks_df, use_container_width=True)

# === ETF selezionati ===
etfs = data.get("etf", [])
st.subheader("🌍 ETF Selezionati")
etf_df = pd.DataFrame(etfs)
st.dataframe(etf_df, use_container_width=True)

# === Grafici ETF ===
st.subheader("📊 Analisi ETF")
if not etf_df.empty:
    chart = alt.Chart(etf_df).mark_bar().encode(
        x=alt.X("name", sort="-y"),
        y="aum_eur_m",
        color="distribution",
        tooltip=["ticker", "ter", "aum_eur_m", "distribution"]
    ).properties(title="AUM per ETF (in milioni €)", height=400)
    st.altair_chart(chart, use_container_width=True)

# === Download CSV ===
st.subheader("📁 Esportazione")
col1, col2 = st.columns(2)
col1.download_button("⬇️ Scarica Titoli CSV", stocks_df.to_csv(index=False), file_name="stocks.csv", mime="text/csv")
col2.download_button("⬇️ Scarica ETF CSV", etf_df.to_csv(index=False), file_name="etf.csv", mime="text/csv")

# === Validazione ===
st.subheader("✅ Validazione Agenti")
st.json(data.get("validation", {}))
st.success(data.get("summary", ""))