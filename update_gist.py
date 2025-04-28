import requests
import json
import os
from datetime import datetime
from bs4 import BeautifulSoup

# ID della tua Gist
GIST_ID = "53990edbd04b6a9a12c6d18e5e618b7e"

# Nome del file dentro la Gist
GIST_FILENAME = "data.json"

# Carica il token GitHub dall'ambiente
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def scrape_news():
    """
    Fa scraping delle ultime notizie da orizzontescuola.it
    """
    url = "https://www.orizzontescuola.it/"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/123.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "it-IT,it;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1"
    }

    session = requests.Session()
    response = session.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    news_list = []

    articles = soup.select("article")
    for article in articles[:5]:  # Prendiamo solo i primi 5 articoli
        title_element = article.select_one("h3")
        link_element = article.select_one("a")

        if title_element and link_element:
            news = {
                "titolo": title_element.get_text(strip=True),
                "descrizione": title_element.get_text(strip=True),
                "link": link_element["href"]
            }
            news_list.append(news)

    return news_list

def generate_data():
    news = scrape_news()
    data = {
        "news": news,
        "aggiornato_il": datetime.utcnow().isoformat() + "Z"
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
