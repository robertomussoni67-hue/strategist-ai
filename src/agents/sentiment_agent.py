import logging
from nltk.sentiment.vader import SentimentIntensityAnalyzer

log = logging.getLogger(__name__)

def run():
    # === Frasi da analizzare ===
    texts = [
        "Markets rally as inflation fears ease",
        "Tech stocks plunge amid rate hike concerns",
        "Investors remain cautious ahead of earnings season",
        "Strong job data boosts confidence in recovery",
        "Global slowdown worries weigh on sentiment"
    ]

    # === Analisi con VADER ===
    analyzer = SentimentIntensityAnalyzer()
    scores = [analyzer.polarity_scores(t)["compound"] for t in texts]
    avg_score = round(sum(scores) / len(scores), 4)

    # === Interpretazione ===
    if avg_score > 0.2:
        sentiment = "positive"
    elif avg_score < -0.2:
        sentiment = "negative"
    else:
        sentiment = "neutral"

    log.info(f"[Sentiment] Frasi analizzate: {len(texts)} → compound medio: {avg_score}")
    for t, s in zip(texts, scores):
        log.info(f"[Sentiment] '{t}' → compound: {s}")

    return {
        "market_sentiment": sentiment,
        "confidence": avg_score,
        "details": {
            "texts_analyzed": len(texts),
            "average_compound": avg_score,
            "individual_scores": scores
        }
    }