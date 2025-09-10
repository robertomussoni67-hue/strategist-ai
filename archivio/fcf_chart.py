import matplotlib.pyplot as plt

# Dati storici
years = [2020, 2021, 2022, 2023, 2024]
fcf_data = {
    "AAPL": [73.37, 92.95, 111.44, 99.58, 108.81],
    "MSFT": [45.23, 65.15, 59.48, 74.07, 71.61],
    "GOOG": [42.84, 67.01, 60.01, 69.50, 72.76],
    "AMZN": [31.02, -9.07, -11.57, 36.81, 38.22],
    "META": [23.63, 39.12, 19.29, 44.07, 54.07]
}

# Colori personalizzati
colors = {
    "AAPL": "#1f77b4",
    "MSFT": "#ff7f0e",
    "GOOG": "#2ca02c",
    "AMZN": "#9467bd",
    "META": "#d62728"
}

# Creazione della figura con due grafici affiancati
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# --- Grafico a linee (storico) ---
for company, values in fcf_data.items():
    ax1.plot(years, values, marker='o', label=company, color=colors[company])
    for x, y in zip(years, values):
        ax1.text(x, y + 2, f"{y:.1f}", ha='center', fontsize=8)

ax1.set_title("Free Cash Flow Storico (miliardi USD)")
ax1.set_xlabel("Anno")
ax1.set_ylabel("FCF (mld USD)")
ax1.grid(True, linestyle='--', alpha=0.5)
ax1.legend()

# --- Grafico a barre (2024) ---
companies = list(fcf_data.keys())
values_2024 = [fcf_data[c][-1] for c in companies]
bars = ax2.bar(companies, values_2024, color=[colors[c] for c in companies])

for bar, val in zip(bars, values_2024):
    ax2.text(bar.get_x() + bar.get_width()/2, val + 1, f"{val:.1f}", ha='center', fontsize=9)

ax2.set_title("Free Cash Flow - Anno 2024 (miliardi USD)")
ax2.set_ylabel("FCF (mld USD)")
ax2.grid(axis='y', linestyle='--', alpha=0.5)

# Ottimizzazione layout
plt.tight_layout()

# --- Salvataggio in PNG ---
plt.savefig("fcf_chart.png", dpi=300)

plt.show()