import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# Scarica il dizionario VADER (solo la prima volta)
nltk.download('vader_lexicon', quiet=True)

# Inizializza una sola volta
sia = SentimentIntensityAnalyzer()

def analizza_sentiment(testo):
    punteggi = sia.polarity_scores(testo.strip())
    compound = punteggi['compound']

    if compound >= 0.05:
        sentiment = 'Positivo 🟢'
    elif compound <= -0.05:
        sentiment = 'Negativo 🔴'
    else:
        sentiment = 'Neutro 🟡'

    return {
        'testo': testo,
        'sentiment': sentiment,
        'dettagli': punteggi
    }

if __name__ == "__main__":
    print("\n🔍 Analisi Sentimentale")
    print("----------------------")
    print("Scrivi una frase per volta. Digita 'exit' per uscire.\n")

    while True:
        testo_input = input("Testo: ")
        if testo_input.lower().strip() == 'exit':
            print("👋 Fine analisi.")
            break

        risultato = analizza_sentiment(testo_input)
        print(f"→ Sentiment: {risultato['sentiment']}")
        print(f"  Dettagli: {risultato['dettagli']}\n")