import streamlit as st
import pandas as pd
import json
from risk_engine import apply_user_filters

# Credenziali utente
users = {
    "sonia": {"password": "strategist2025", "config": "config_sonia.json"}
}

st.title("Strategist AI - Accesso Privato")

# Login
username = st.text_input("Username")
password = st.text_input("Password", type="password")

if username in users and password == users[username]["password"]:
    st.success(f"Benvenuta, {username}!")

    # Carica profilo JSON
    with open(users[username]["config"], "r", encoding="utf-8") as f:
        profile = json.load(f)

    st.subheader("Profilo Strategist")
    st.json(profile)

    # Caricamento portafoglio
    st.subheader("📂 Carica il tuo portafoglio (CSV)")
    uploaded_file = st.file_uploader("Scegli file CSV", type="csv")

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.write("📊 Portafoglio originale:")
        st.dataframe(df)

        # Analisi rischio
        df_filtered = apply_user_filters(df, profile)
        st.write("📈 Analisi del rischio:")
        st.dataframe(df_filtered)

        # Pulsante download
        st.download_button(
            "Scarica risultati",
            df_filtered.to_csv(index=False),
            "analisi_portafoglio.csv",
            "text/csv"
        )
else:
    st.warning("Inserisci credenziali valide")
    st.stop()