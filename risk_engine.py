import os
import csv

CSV_PATH = "analisi_aziende.csv"

def crea_csv_se_manca():
    if not os.path.exists(CSV_PATH):
        with open(CSV_PATH, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([
                "ID", "Nome", "Valore Intrinseco (€)", "Indice Rischio",
                "Debt/Equity", "Current Ratio", "Interest Coverage"
            ])
        print(f"✅ Creato file CSV: {CSV_PATH}")

def calcola_dcf(fcf_attuale, crescita, anni, tasso_sconto, crescita_terminal):
    flussi_scontati = 0
    fcf = fcf_attuale
    for anno in range(1, anni + 1):
        fcf *= (1 + crescita)
        flussi_scontati += fcf / ((1 + tasso_sconto) ** anno)
    terminal_value = (fcf * (1 + crescita_terminal)) / (tasso_sconto - crescita_terminal)
    terminal_scontato = terminal_value / ((1 + tasso_sconto) ** anni)
    return flussi_scontati + terminal_scontato

def aggiungi_azienda(id_val, nome, fcf_attuale, crescita, anni, tasso_sconto, crescita_terminal,
                     debito_tot, patrimonio_netto, att_correnti, pass_correnti, ebit, oneri_fin, indice_rischio):
    valore_intrinseco = calcola_dcf(fcf_attuale, crescita, anni, tasso_sconto, crescita_terminal)
    debt_equity = debito_tot / patrimonio_netto if patrimonio_netto else 0
    current_ratio = att_correnti / pass_correnti if pass_correnti else 0
    interest_cov = ebit / oneri_fin if oneri_fin else 0

    with open(CSV_PATH, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            id_val, nome, round(valore_intrinseco, 2), round(indice_rischio, 2),
            round(debt_equity, 2), round(current_ratio, 2), round(interest_cov, 2)
        ])
    print(f"📈 Aggiunta analisi per {nome}")

def leggi_csv():
    if os.path.exists(CSV_PATH):
        with open(CSV_PATH, mode="r", encoding="utf-8") as file:
            for riga in csv.reader(file):
                print(riga)
    else:
        print("❌ Nessun file trovato.")

if __name__ == "__main__":
    crea_csv_se_manca()

    while True:
        print("\n--- Menu ---")
        print("1. Aggiungi azienda")
        print("2. Visualizza dati")
        print("3. Esci")
        scelta = input("Scelta: ").strip()

        if scelta == "1":
            try:
                id_val = int(input("ID: "))
                nome = input("Nome azienda: ")
                fcf_attuale = float(input("Free Cash Flow attuale (€): "))
                crescita = float(input("Tasso di crescita previsto (es. 0.05 per 5%): "))
                anni = int(input("Anni di previsione: "))
                tasso_sconto = float(input("Tasso di sconto (es. 0.1 per 10%): "))
                crescita_terminal = float(input("Crescita perpetua terminale (es. 0.02 per 2%): "))
                debito_tot = float(input("Debito totale (€): "))
                patrimonio_netto = float(input("Patrimonio netto (€): "))
                att_correnti = float(input("Attività correnti (€): "))
                pass_correnti = float(input("Passività correnti (€): "))
                ebit = float(input("EBIT (€): "))
                oneri_fin = float(input("Oneri finanziari (€): "))
                indice_rischio = float(input("Indice di rischio (0-1): "))

                aggiungi_azienda(id_val, nome, fcf_attuale, crescita, anni, tasso_sconto, crescita_terminal,
                                 debito_tot, patrimonio_netto, att_correnti, pass_correnti, ebit, oneri_fin, indice_rischio)
            except ValueError:
                print("⚠️ Inserisci solo numeri dove richiesto.")
        elif scelta == "2":
            leggi_csv()
        elif scelta == "3":
            break
        else:
            print("⚠️ Scelta non valida.")