def explain_plan(plan, regime, sentiment, profile):
    explanations = []

    for asset in plan:
        ticker = asset.get("ticker", "")
        name = asset.get("name", "")
        weight = round(asset.get("weight", 0), 4)
        type_ = asset.get("type", "")

        if type_ == "STOCK":
            if ticker == "JNJ":
                reason = "difensiva e stabile nei periodi recessivi"
            elif ticker == "MSFT":
                reason = "tecnologica con solidi fondamentali e cash flow"
            elif ticker == "NVDA":
                reason = "esposizione a settori innovativi come AI e semiconduttori"
            else:
                reason = "titolo selezionato per resilienza e qualità"

        elif type_ == "ETF":
            if "VWCE" in ticker:
                reason = "esposizione globale con TER contenuto e AUM elevato"
            elif ticker == "AGGH":
                reason = "diversificazione obbligazionaria globale"
            elif ticker == "SPY":
                reason = "copertura sul mercato USA con alta liquidità"
            else:
                reason = "ETF selezionato per coerenza con regime e profilo"

        else:
            reason = "strumento selezionato per bilanciare il portafoglio"

        explanations.append(
            f"- {ticker} ({name}): peso {weight*100:.2f}% → scelto perché {reason}."
        )

    summary = f"""
📋 Piano allocativo per {profile.name}, profilo {profile.risk_level}, regime attuale: {regime}, sentiment: {sentiment}

Le scelte riflettono la filosofia '{profile.style}' e l'obiettivo '{profile.goal}'.
Ecco le motivazioni principali:
""" + "\n".join(explanations)

    return summary.strip()