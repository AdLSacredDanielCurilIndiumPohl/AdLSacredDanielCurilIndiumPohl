FROM mongo:latest

# Umgebungsvariablen für Cluster-Konfiguration
ENV MONGO_INITDB_ROOT_USERNAME=admin
ENV MONGO_INITDB_ROOT_PASSWORD_FILE=/run/secrets/mongo_password
ENV MONGO_INITDB_DATABASE=ordo_connectoris

# Healthcheck konfigurieren
HEALTHCHECK --interval=30s --timeout=3s \
    CMD mongosh --eval "db.adminCommand('ping')" || exit 1

# Ports exponieren (Standard MongoDB + Cluster Kommunikation)
EXPOSE 27017 27018 27019

# Volume für persistente Daten
VOLUME /data/db

# Initialisierungsskript kopieren
COPY init-mongo.js /docker-entrypoint-initdb.d/