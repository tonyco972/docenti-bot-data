import axios from 'axios';
import fs from 'fs';
import { parseStringPromise } from 'xml2js';

const url = 'https://www.orizzontescuola.it/feed/';

async function fetchNews() {
  try {
    const { data } = await axios.get(url);
    const result = await parseStringPromise(data);

    const items = result.rss.channel[0].item;

    const news = items.map(item => ({
      titolo: item.title[0],
      link: item.link[0],
      descrizione: item.description[0],
      data: item.pubDate[0]
    }));

    fs.writeFileSync('docenti-news.json', JSON.stringify(news, null, 2));
    console.log(`✅ Salvate ${news.length} news in docenti-news.json`);
  } catch (err) {
    console.error('❌ Errore durante il recupero delle news:', err.message);
    process.exit(1);
  }
}

fetchNews();
