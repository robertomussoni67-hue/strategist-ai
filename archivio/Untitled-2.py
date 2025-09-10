def execute_macro(command):
    if command == "start":
        print("Avvio strategia principale...")

        # 📊 1) Raccolta dati macro e rilevamento regime
        macro = get_macro_data()
        regime = detect_regime(macro)
        print(f"Dati macro: {macro}")
        print(f"Regime di mercato rilevato: {regime.upper()}")

        # 📈 2) Analisi ETF
        try:
            from modules import subagent_etf
            subagent_etf.run_etf_analysis(regime)
        except ImportError:
            print("Modulo subagent_etf non trovato o non valido.")

        # 💹 3) Analisi Azioni
        try:
            from modules import subagent_stocks
            stocks = subagent_stocks.analyze_stocks(regime)
            print(f"\n[AZIONI] Selezionate per regime '{regime}':")
            for stock in stocks:
                print(f" - {stock['ticker']} | {stock['name']} | Settore: {stock['sector']} | Prezzo: {stock['price']}")
        except ImportError:
            print("Modulo subagent_stocks non trovato o non valido.")

        print("\nStrategia attiva ✅")

    elif command == "report":
        print("Eseguo macro: report...")

        try:
            macro = get_macro_data()
            regime = detect_regime(macro)
            print(f"Dati macro: {macro}")
            print(f"Regime di mercato rilevato: {regime.upper()}")
        except NameError:
            print("Funzioni get_macro_data/detect_regime non disponibili.")
        except Exception as e:
            print(f"Errore durante la generazione del report: {e}")

    else:
        print(f"Comando '{command}' non riconosciuto.")
        print("Comandi disponibili: start, report")
        print("Uso: python strategist.py <comando>")