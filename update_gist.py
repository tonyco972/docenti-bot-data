import requests
import json
import os

# ID della tua Gist
GIST_ID = "47554691172b680172f003458025d7c3"

# Nome del file dentro la gist (deve esistere già)
GIST_FILENAME = "data.json"

# Carica il token segreto dalle variabili di ambiente
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# --- Qui generi i dati che vuoi caricare ---
def generate_data():
    # Esempio di dati fittizi
    data = {
        "message": "Buongiorno, docenti!",
        "timestamp": "2025-04-28T10:00:00"
    }
    return data

def update_gist(content):
    url = f"https://api.github.com/gists/{GIST_ID}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
    }
    payload = {
        "files": {
            GIST_FILENAME: {
                "content": content
            }
        }
    }
    response = requests.patch(url, headers=headers, json=payload)
    if response.status_code == 200:
        print("✅ Gist aggiornata con successo!")
    else:
        print(f"❌ Errore nell'aggiornare la Gist: {response.status_code}")
        print(response.text)

def main():
    data = generate_data()
    json_content = json.dumps(data, indent=2, ensure_ascii=False)
    update_gist(json_content)

if __name__ == "__main__":
    main()
