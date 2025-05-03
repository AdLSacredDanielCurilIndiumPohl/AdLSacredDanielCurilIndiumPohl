import fs from 'fs';
import path from 'path';
import { exec } from 'child_process';

const infraPath = path.resolve('./infra');

// Orchestrator für alle Instanzen
function startInstances() {
  console.log('✨ Orchestrator startet alle Instanzen...');

  fs.readdirSync(infraPath).forEach(file => {
    if (file.endsWith('.js') && file !== 'orchestrator.js') {
      const instancePath = path.join(infraPath, file);
      console.log(`🚀 Starte Instanz: ${file}`);
      exec(`node ${instancePath}`, (err, stdout, stderr) => {
        if (err) {
          console.error(`❌ Fehler beim Starten von ${file}:`, err);
        } else {
          console.log(`✅ Instanz ${file} gestartet.`);
          console.log(stdout);
        }
      });
    }
  });
}

startInstances();
