import express from 'express';
import { exec } from 'child_process';

const app = express();
const PORT = process.env.PORT || 3000;

// Liste der verfügbaren Tools
const tools = [
  { name: 'MCP-Server', command: 'docker run -d mcp-server' },
  { name: 'HPC-Server', command: 'docker run -d hpc-server' },
  { name: 'API-Tool', command: 'docker run -d api-tool' },
];

// API-Endpunkt für die Tool-Bar
app.get('/tools', (req, res) => {
  res.json(tools);
});

// API-Endpunkt zum Starten eines Tools
app.post('/start/:tool', (req, res) => {
  const tool = tools.find(t => t.name === req.params.tool);
  if (tool) {
    exec(tool.command, (err, stdout, stderr) => {
      if (err) {
        res.status(500).send(`Fehler beim Starten von ${tool.name}: ${stderr}`);
      } else {
        res.send(`${tool.name} wurde gestartet: ${stdout}`);
      }
    });
  } else {
    res.status(404).send('Tool nicht gefunden');
  }
});

app.listen(PORT, () => {
  console.log(`Tool-Bar läuft auf http://localhost:${PORT}`);
});
