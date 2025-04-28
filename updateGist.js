import fs from 'fs';
import https from 'https';

const token = process.env.GITHUB_TOKEN;
const gistId = process.env.GIST_ID;
const newsData = fs.readFileSync('docenti-news.json', 'utf8');

const payload = {
  files: {
    'docenti-news.json': {
      content: newsData
    }
  }
};

const options = {
  hostname: 'api.github.com',
  path: `/gists/${gistId}`,
  method: 'PATCH',
  headers: {
    'User-Agent': 'Node.js',
    'Authorization': `token ${token}`,
    'Content-Type': 'application/json',
    'Accept': 'application/vnd.github.v3+json'
  }
};

const req = https.request(options, (res) => {
  let data = '';
  res.on('data', (chunk) => data += chunk);
  res.on('end', () => {
    if (res.statusCode >= 200 && res.statusCode < 300) {
      console.log('✅ Gist aggiornato con successo!');
    } else {
      console.error(`❌ Errore: ${res.statusCode}`);
      console.error(data);
      process.exit(1);
    }
  });
});

req.on('error', (error) => {
  console.error(`❌ Errore di rete: ${error.message}`);
  process.exit(1);
});

req.write(JSON.stringify(payload));
req.end();
