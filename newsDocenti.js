import axios from 'axios';
import * as cheerio from 'cheerio';
import fs from 'fs';

const url = 'https://www.orizzontescuola.it/';

async function fetchNews() {
  try {
    const { data } = await axios.get(url);
    const $ = cheerio.load(data);

    const news = [];

    $('.jeg_postblock_content .jeg_post_title a').each((i, el) => {
      const titolo = $(el).text().trim();
      const link = $(el).attr('href');
      const descrizione = "Leggi l'articolo completo su Orizzonte Scuola.";
      const dataPubblicazione = new Date().toISOString().split('T')[0];

      news.push({
        titolo,
        link,
        descrizione,
        data: dataPubblicazione
      });
    });

    fs.writeFileSync('docenti-news.json', JSON.stringify(news, null, 2));
    console.log(`✅ Salvate ${news.length} news in docenti-news.json`);
  } catch (err) {
    console.error('❌ Errore durante lo scraping:', err.message);
    process.exit(1);
  }
}

fetchNews();
