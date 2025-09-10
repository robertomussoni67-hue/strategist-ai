import json
import firebase_admin
from firebase_admin import credentials, firestore

# === CONFIGURAZIONE FIREBASE ===
# Usa direttamente il file originale della chiave di servizio
cred = credentials.Certificate("config/firebase_service_account.json")

# Inizializza Firebase (evita doppia inizializzazione)
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

# Crea il client Firestore
db = firestore.client()

# === ESEMPIO DI SCRITTURA SU FIRESTORE ===
# Qui puoi adattare la logica di Strategist
app_id = "strategist-app"
user_id = "roberto"

# Percorso: artifacts/strategist-app/users/roberto/strategist_results/test_doc
doc_ref = (
    db.collection("artifacts")
      .document(app_id)
      .collection("users")
      .document(user_id)
      .collection("strategist_results")
      .document("test_doc")
)

doc_ref.set({
    "messaggio": "Connessione riuscita da Strategist!",
    "timestamp": firestore.SERVER_TIMESTAMP
})

print("✅ Documento di test salvato su Firestore")