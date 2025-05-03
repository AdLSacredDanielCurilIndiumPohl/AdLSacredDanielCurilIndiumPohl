FROM postgres:latest

# Umgebungsvariablen für initiale Datenbank-Konfiguration
ENV POSTGRES_DB=ordo_connectoris
ENV POSTGRES_USER=admin
ENV POSTGRES_PASSWORD_FILE=/run/secrets/postgres_password

# Healthcheck konfigurieren
HEALTHCHECK --interval=30s --timeout=3s \
    CMD pg_isready -U $POSTGRES_USER -d $POSTGRES_DB || exit 1

# Port exponieren
EXPOSE 5432

# Volume für persistente Daten
VOLUME /var/lib/postgresql/data