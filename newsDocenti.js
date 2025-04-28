import axios from 'axios';
import cheerio from 'cheerio';
import fs from 'fs';

const url = 'https://www.orizzontescuola.it/';

async function estraiNews() {
  try {
    const { data } = await axios.get(url);
    const $ = cheerio.load(data);

    const news = [];

    $('.jeg_postblock_content .jeg_post_title > a').each((i, elem) => {
      if (i < 10) {
        const titolo = $(elem).text().trim();
        const link = $(elem).attr('href');
        const dataPubblicazione = new Date().toISOString().slice(0, 10);

        news.push({
          titolo,
          link,
          data: dataPubblicazione
        });
      }
    });

    fs.writeFileSync('docenti-news.json', JSON.stringify(news, null, 2));
    console.log('✅ File docenti-news.json aggiornato');

  } catch (error) {
    console.error('❌ Errore durante lo scraping:', error);
  }
}

estraiNews();
