#!/bin/bash

# Vault starten
vault server -config=config.hcl &

# Warten bis Vault bereit ist
sleep 5

# Vault initialisieren
vault operator init > /vault-data/init.txt

# Root Token und Unseal Keys extrahieren
export VAULT_TOKEN=$(grep 'Initial Root Token:' /vault-data/init.txt | awk '{print $NF}')
export UNSEAL_KEY_1=$(grep 'Unseal Key 1:' /vault-data/init.txt | awk '{print $NF}')

# Vault entsiegeln
vault operator unseal $UNSEAL_KEY_1

# Secrets Engine aktivieren
vault secrets enable -path=database database
vault secrets enable -path=secret kv-v2

# Datenbank-Credentials einrichten
vault write database/config/postgresql \
    plugin_name=postgresql-database-plugin \
    connection_url="postgresql://{{username}}:{{password}}@postgres:5432/ordo_connectoris" \
    allowed_roles="*" \
    username="admin" \
    password="${POSTGRES_PASSWORD}"

vault write database/config/mongodb \
    plugin_name=mongodb-database-plugin \
    connection_url="mongodb://{{username}}:{{password}}@mongodb:27017/admin" \
    allowed_roles="*" \
    username="admin" \
    password="${MONGO_PASSWORD}"

vault write database/config/redis \
    plugin_name=redis-database-plugin \
    connection_url="redis://{{username}}:{{password}}@redis:6379/0" \
    allowed_roles="*" \
    username="default" \
    password="${REDIS_PASSWORD}"

# Semantic Orchestrator Token generieren
vault token create -policy="db-admin" -display-name="semantic-orchestrator" > /vault-data/orchestrator-token.txt

echo "Vault initialization complete. Credentials stored in /vault-data/"