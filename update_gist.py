import json
import os
import requests  # Aggiunto import per requests
from datetime import datetime, timezone
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

# ID della tua Gist
GIST_ID = "47554691172b680172f003458025d7c3"
GIST_FILENAME = "data.json"

# Carica il token GitHub dall'ambiente
GITHUB_TOKEN = os.getenv("PERSONAL_GIST_TOKEN
")

def scrape_news():
    """
    Fa scraping delle ultime notizie da orizzontescuola.it
    Usando Playwright per emulare un browser vero
    """
    url = "https://www.orizzontescuola.it/"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)

        # Ottieni il contenuto HTML della pagina
        html_content = page.content()

        # Usa BeautifulSoup per il parsing
        soup = BeautifulSoup(html_content, "html.parser")
        
        news_list = []

        articles = soup.select("article")  # Prendi gli articoli
        for article in articles[:5]:  # Prendi solo i primi 5 articoli
            title_element = article.select_one("h3")
            link_element = article.select_one("a")

            if title_element and link_element:
                news = {
                    "titolo": title_element.get_text(strip=True),
                    "descrizione": title_element.get_text(strip=True),
                    "link": link_element["href"]
                }
                news_list.append(news)

        browser.close()

    return news_list

def generate_data():
    news = scrape_news()
    data = {
        "news": news,
        "aggiornato_il": datetime.now(timezone.utc).isoformat()  # Usa ora UTC
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
