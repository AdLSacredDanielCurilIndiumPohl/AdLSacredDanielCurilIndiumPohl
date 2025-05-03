#!/usr/bin/env python3
import os
import sys
import uuid
import json
import hashlib
import docker
from pathlib import Path

def create_tool_container(tool_name, tool_path, tool_config):
    """Erstellt einen isolierten Container für ein Tool"""
    
    # Generiere eine eindeutige ID für das Tool
    tool_id = hashlib.sha256(tool_name.encode()).hexdigest()[:12]
    
    # Erstelle Dockerfile für das Tool
    dockerfile = f"""
FROM python:3.9-slim

WORKDIR /tool
ENV TOOL_ID={tool_id}
ENV TOOL_SECRET={uuid.uuid4()}

# Sicherheits-Hardening
RUN useradd -m -s /bin/bash tool_user && \
    chown -R tool_user:tool_user /tool

# Kopiere Tool und Dependencies
COPY --chown=tool_user:tool_user {tool_path} /tool/
COPY --chown=tool_user:tool_user requirements.txt /tool/

# Installiere Dependencies
RUN pip install --no-cache-dir -r requirements.txt

USER tool_user

# Starte Tool mit eingeschränkten Rechten
CMD ["python", "main.py"]
"""
    
    # Erstelle Tool-Container
    client = docker.from_env()
    
    # Baue Image
    image, _ = client.images.build(
        path=".",
        dockerfile=dockerfile,
        tag=f"registry.local:5000/tool/{tool_name}:{tool_id}"
    )
    
    # Pushe zu privater Registry
    client.images.push(
        f"registry.local:5000/tool/{tool_name}",
        tag=tool_id
    )
    
    # Registriere Tool im Auth-Service
    tool_config.update({
        "id": tool_id,
        "image": f"registry.local:5000/tool/{tool_name}:{tool_id}",
        "access_url": f"/tools/{tool_id}"
    })
    
    return tool_config

def main(tool_csv):
    """Hauptfunktion zum Deployment der Tools"""
    
    with open(tool_csv) as f:
        tools = json.load(f)
    
    deployed_tools = []
    
    for tool in tools:
        try:
            config = create_tool_container(
                tool["name"],
                tool["path"],
                tool["config"]
            )
            deployed_tools.append(config)
        except Exception as e:
            print(f"Fehler beim Deployment von {tool['name']}: {e}")
            continue
    
    # Speichere Deployment-Konfiguration
    with open("deployed_tools.json", "w") as f:
        json.dump(deployed_tools, f, indent=2)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: deploy_tool.py <tools.json>")
        sys.exit(1)
    
    main(sys.argv[1])