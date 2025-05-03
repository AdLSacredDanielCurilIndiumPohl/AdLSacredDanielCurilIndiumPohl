import { createServer } from 'http';

// Einfaches Interface für Instanz-Interaktionen
const instanceData = {
  status: 'active',
  name: 'GIGA•TENANT•INSTANCE',
  created: new Date().toISOString(),
};

createServer((req, res) => {
  if (req.url === '/status') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(instanceData));
  } else {
    res.writeHead(404);
    res.end('Not Found');
  }
}).listen(process.env.PORT || 4000, '127.0.0.1', () => {
  console.log('Instance Interface läuft auf Port 4000');
});
