#!/bin/bash
echo "✨ Initialisiere GIGA•TENANT..."
npm install
echo "✅ Bereit für den Kosmos."

# Installiere globale Tools
function install_global_tools() {
  echo "✨ Installiere globale Tools..."

  # Docker installieren
  if ! command -v docker &> /dev/null; then
    echo "🐳 Docker wird installiert..."
    sudo apt-get update && sudo apt-get install -y docker.io
  else
    echo "🐳 Docker ist bereits installiert."
  fi

  # Node.js-Pakete installieren
  echo "📦 Installiere globale Node.js-Pakete..."
  npm install -g nodemon

  # AWS CLI installieren
  if ! command -v aws &> /dev/null; then
    echo "☁️ AWS CLI wird installiert..."
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
    unzip awscliv2.zip
    sudo ./aws/install
    rm -rf awscliv2.zip aws/
  else
    echo "☁️ AWS CLI ist bereits installiert."
  fi

  # Google Cloud SDK installieren
  if ! command -v gcloud &> /dev/null; then
    echo "☁️ Google Cloud SDK wird installiert..."
    echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] http://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
    sudo apt-get install -y apt-transport-https ca-certificates
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
    sudo apt-get update && sudo apt-get install -y google-cloud-sdk
  else
    echo "☁️ Google Cloud SDK ist bereits installiert."
  fi

  # MongoDB installieren
  if ! command -v mongod &> /dev/null; then
    echo "🍃 MongoDB wird installiert..."
    wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add -
    echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/4.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.4.list
    sudo apt-get update && sudo apt-get install -y mongodb-org
  else
    echo "🍃 MongoDB ist bereits installiert."
  fi

  # Postman installieren
  if ! command -v postman &> /dev/null; then
    echo "📬 Postman wird installiert..."
    sudo snap install postman
  else
    echo "📬 Postman ist bereits installiert."
  fi

  # Datadog Agent installieren
  if ! command -v datadog-agent &> /dev/null; then
    echo "📊 Datadog Agent wird installiert..."
    DD_AGENT_MAJOR_VERSION=7 DD_API_KEY=your_api_key DD_SITE="datadoghq.com" bash -c "$(curl -L https://s3.amazonaws.com/dd-agent/scripts/install_script.sh)"
  else
    echo "📊 Datadog Agent ist bereits installiert."
  fi

  # MCP-Server installieren
  echo "🔧 Installiere MCP-Server..."
  if ! command -v mcp-server &> /dev/null; then
    echo "🌐 MCP-Server wird installiert..."
    npm install -g mcp-server
  else
    echo "🌐 MCP-Server ist bereits installiert."
  fi

  # HPC-Server installieren
  echo "🔧 Installiere HPC-Server..."
  if ! command -v hpc-server &> /dev/null; then
    echo "⚡ HPC-Server wird installiert..."
    npm install -g hpc-server
  else
    echo "⚡ HPC-Server ist bereits installiert."
  fi

  # APIs installieren
  echo "🔧 Installiere APIs..."
  npm install express axios
}

# MCP-Tools installieren
function install_mcp_tools() {
  echo "🔧 Installiere MCP-Tools..."

  # Beispiel-Tool 1: MCP-Analyzer
  if ! command -v mcp-analyzer &> /dev/null; then
    echo "📊 MCP-Analyzer wird installiert..."
    npm install -g mcp-analyzer
  else
    echo "📊 MCP-Analyzer ist bereits installiert."
  fi

  # Beispiel-Tool 2: MCP-Manager
  if ! command -v mcp-manager &> /dev/null; then
    echo "🛠️ MCP-Manager wird installiert..."
    npm install -g mcp-manager
  else
    echo "🛠️ MCP-Manager ist bereits installiert."
  fi

  # Beispiel-Tool 3: MCP-Dashboard
  if ! command -v mcp-dashboard &> /dev/null; then
    echo "📈 MCP-Dashboard wird installiert..."
    npm install -g mcp-dashboard
  else
    echo "📈 MCP-Dashboard ist bereits installiert."
  fi
}

# MCP-Server-Repositories klonen und installieren
function install_mcp_servers() {
  echo "🔧 Klone und installiere MCP-Server-Repositories..."

  # Liste der Repositories
  declare -a repos=(
    "https://github.com/punkpeye/awesome-mcp-servers"
    "https://github.com/activepieces/activepieces"
    "https://github.com/github/github-mcp-server"
    "https://github.com/microsoft/playwright-mcp"
    "https://github.com/jlowin/fastmcp"
  )

  # Zielverzeichnis für die Repositories
  local target_dir="mcp_servers"
  mkdir -p "$target_dir"

  # Repositories klonen und installieren
  for repo in "${repos[@]}"; do
    repo_name=$(basename "$repo" .git)
    if [ ! -d "$target_dir/$repo_name" ]; then
      echo "🌐 Klone $repo..."
      git clone "$repo" "$target_dir/$repo_name"
      if [ -f "$target_dir/$repo_name/package.json" ]; then
        echo "📦 Installiere Abhängigkeiten für $repo_name..."
        (cd "$target_dir/$repo_name" && npm install)
      fi
    else
      echo "✅ $repo_name ist bereits vorhanden."
    fi
  done
}

# Zusätzliche MCP-Server-Repositories klonen und installieren
function install_additional_mcp_servers() {
  echo "🔧 Klone und installiere zusätzliche MCP-Server-Repositories..."

  # Liste der zusätzlichen Repositories
  declare -a additional_repos=(
    "https://github.com/1Panel-dev/1Panel.git"
    "https://github.com/Riteo/godot.git"
    "https://github.com/phi-go/rfcs.git"
    "https://github.com/amolnar-rh/openshift-docs.git"
    "https://github.com/GLips/Figma-Context-MCP.git"
    "https://github.com/LaurieWired/GhidraMCP.git"
    "https://github.com/lharries/whatsapp-mcp.git"
    "https://github.com/OPS-E2E-PPE/split-ref-ppe.git"
    "https://github.com/VilnaCRM-Org/website.git"
  )

  # Zielverzeichnis für die zusätzlichen Repositories
  local target_dir="additional_mcp_servers"
  mkdir -p "$target_dir"

  # Repositories klonen und installieren
  for repo in "${additional_repos[@]}"; do
    repo_name=$(basename "$repo" .git)
    if [ ! -d "$target_dir/$repo_name" ]; then
      echo "🌐 Klone $repo..."
      git clone "$repo" "$target_dir/$repo_name"
      if [ -f "$target_dir/$repo_name/package.json" ]; then
        echo "📦 Installiere Abhängigkeiten für $repo_name..."
        (cd "$target_dir/$repo_name" && npm install)
      fi
    else
      echo "✅ $repo_name ist bereits vorhanden."
    fi
  done
}

# Installiere und orchestriere alle MCP-, HPC- und API-Instanzen
function install_and_orchestrate_instances() {
  echo "🔧 Installiere und orchestriere alle Instanzen..."

  # Verzeichnisse mit Repositories
  declare -a directories=(
    "additional_mcp_servers"
    "mcp_servers"
  )

  # Installiere Abhängigkeiten und starte Instanzen
  for dir in "${directories[@]}"; do
    for repo in "$dir"/*; do
      if [ -d "$repo" ]; then
        echo "📦 Installiere Abhängigkeiten für $repo..."
        if [ -f "$repo/package.json" ]; then
          (cd "$repo" && npm install)
        elif [ -f "$repo/requirements.txt" ]; then
          (cd "$repo" && pip install -r requirements.txt)
        elif [ -f "$repo/go.mod" ]; then
          (cd "$repo" && go mod tidy)
        fi

        # Starte Instanz, falls anwendbar
        if [ -f "$repo/main.js" ]; then
          echo "🚀 Starte Node.js-Instanz in $repo..."
          (cd "$repo" && node main.js &)
        elif [ -f "$repo/main.py" ]; then
          echo "🚀 Starte Python-Instanz in $repo..."
          (cd "$repo" && python main.py &)
        elif [ -f "$repo/main.go" ]; then
          echo "🚀 Starte Go-Instanz in $repo..."
          (cd "$repo" && go run main.go &)
        fi
      fi
    done
  done

  echo "✅ Alle Instanzen wurden installiert und orchestriert."
}

# Containerisierung und Bereitstellung
function containerize_and_deploy() {
  echo "🔧 Containerisiere und deploye alle Instanzen..."

  # Verzeichnisse mit Repositories
  declare -a directories=(
    "additional_mcp_servers"
    "mcp_servers"
  )

  # Dockerfile erstellen und Container bauen
  for dir in "${directories[@]}"; do
    for repo in "$dir"/*; do
      if [ -d "$repo" ]; then
        echo "🐳 Erstelle Docker-Container für $repo..."
        cat <<EOF > "$repo/Dockerfile"
        FROM node:20-alpine
        WORKDIR /app
        COPY . .
        RUN npm install || true
        CMD ["npm", "start"]
EOF
        (cd "$repo" && docker build -t "$(basename $repo)" .)
      fi
    done
  done

  echo "✅ Alle Instanzen wurden containerisiert."
}

# Hauptinitialisierung
install_global_tools
install_mcp_tools
install_mcp_servers
install_additional_mcp_servers
install_and_orchestrate_instances
containerize_and_deploy

echo "✅ Bereit für den Kosmos."
