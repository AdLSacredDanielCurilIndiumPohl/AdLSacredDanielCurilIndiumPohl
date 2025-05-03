#!/usr/bin/env python3
import os
import json
from pathlib import Path
import subprocess
import hashlib

class ToolImportHandler:
    def __init__(self):
        self.cli_path = os.path.join(os.path.dirname(__file__), "cli_simple.py")
        self.imported_tools = set()
        
    def calculate_tool_hash(self, tool_path):
        """Berechnet einen Hash für die Tool-Definition"""
        sha256_hash = hashlib.sha256()
        with open(tool_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()[:12]
    
    def import_tool(self, tool_path):
        """Importiert ein einzelnes Tool"""
        tool_hash = self.calculate_tool_hash(tool_path)
        if tool_hash in self.imported_tools:
            print(f"Tool {tool_path} wurde bereits importiert")
            return
        
        # Registriere Tool mit CLI
        try:
            tool_name = Path(tool_path).stem
            tool_type = self.detect_tool_type(tool_path)
            
            subprocess.run([
                "python3",
                self.cli_path,
                "register_tool",
                tool_name,
                tool_type
            ], check=True)
            
            self.imported_tools.add(tool_hash)
            print(f"Tool {tool_name} erfolgreich importiert")
            
        except subprocess.CalledProcessError as e:
            print(f"Fehler beim Import von {tool_path}: {e}")
    
    def detect_tool_type(self, tool_path):
        """Erkennt den Tool-Typ basierend auf dem Inhalt"""
        path = Path(tool_path)
        
        if "transzen" in path.stem.lower():
            return "transzen"
        elif "bloomberg" in path.stem.lower():
            return "financial"
        elif "board" in path.stem.lower():
            return "portal"
        elif "cluster" in path.stem.lower():
            return "analytics"
        elif "tools_init_mcp" in path.stem.lower():
            return "mcp"
        else:
            return "general"
    
    def process_directory(self, directory):
        """Verarbeitet alle relevanten Dateien in einem Verzeichnis"""
        path = Path(directory)
        for file_path in path.rglob("*"):
            if file_path.suffix.lower() in ['.csv', '.xlsx', '.xls']:
                print(f"Verarbeite {file_path}")
                self.import_tool(str(file_path))
    
    def save_import_state(self, state_file):
        """Speichert den Import-Status"""
        state = {
            "imported_tools": list(self.imported_tools)
        }
        with open(state_file, "w") as f:
            json.dump(state, f, indent=2)
    
    def load_import_state(self, state_file):
        """Lädt den Import-Status"""
        if os.path.exists(state_file):
            with open(state_file, "r") as f:
                state = json.load(f)
                self.imported_tools = set(state.get("imported_tools", []))

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python3 import_handler.py <directory>")
        sys.exit(1)
    
    handler = ToolImportHandler()
    handler.load_import_state("import_state.json")
    handler.process_directory(sys.argv[1])
    handler.save_import_state("import_state.json")