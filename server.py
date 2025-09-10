from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import asyncio
from app.engine.decision_engine import DecisionEngine
import main_simple as main  # Usa la versione stabile dell'orchestratore

# Inizializza Flask e motore decisionale
app = Flask(__name__, template_folder='templates')
CORS(app)
engine = DecisionEngine("config/philosophies.json")

# Serve la dashboard HTML
@app.route('/')
def home():
    return render_template('dashboard_test.html')

# Endpoint API per analisi
@app.route('/api/run_analysis', methods=['POST'])
def run_analysis_api():
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        report_string = loop.run_until_complete(main.main_orchestrator())
        loop.close()

        # Dati simulati per test
        data = {
            "stocks_data": [
                {"symbol": "MSFT", "ev_ebit": 24, "roic": 0.38, "moat_score": 0.9, "revenue_cagr_5y": 0.14, "insider_buying": True, "ps": 12},
                {"symbol": "AAPL", "ev_ebit": 21, "roic": 0.33, "moat_score": 0.85, "revenue_cagr_5y": 0.11, "insider_buying": False, "ps": 7},
                {"symbol": "TSLA", "ev_ebit": 50, "roic": 0.15, "moat_score": 0.6, "revenue_cagr_5y": 0.50, "insider_buying": True, "ps": 12},
                {"symbol": "CRSP", "ev_ebit": 999, "roic": -0.1, "moat_score": 0.75, "revenue_cagr_5y": 0.60, "insider_buying": True, "ps": 18}
            ],
            "macro_data": {
                "inflation_trend": "up",
                "growth_trend": "down"
            }
        }

        recommendations = engine.generate_recommendations(data)

        return jsonify({
            "report": report_string,
            "recommendations": recommendations
        })

    except Exception as e:
        return jsonify({
            "error": str(e),
            "message": "Si è verificato un errore durante l'esecuzione dell'analisi."
        }), 500

# Avvia il server
if __name__ == '__main__':
    app.run(debug=True, port=5000)