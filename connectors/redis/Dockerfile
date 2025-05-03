FROM redis:latest

# Redis-Konfiguration für Cluster-Modus
ENV REDIS_PASSWORD_FILE=/run/secrets/redis_password
ENV REDIS_PORT=6379

# Kopiere Redis-Konfiguration
COPY redis.conf /usr/local/etc/redis/redis.conf

# Sentinel für Hochverfügbarkeit
COPY sentinel.conf /usr/local/etc/redis/sentinel.conf

# Ports exponieren (Redis + Sentinel)
EXPOSE 6379 26379

# Healthcheck konfigurieren
HEALTHCHECK --interval=30s --timeout=3s \
    CMD redis-cli ping || exit 1

# Volume für persistente Daten
VOLUME /data

CMD ["redis-server", "/usr/local/etc/redis/redis.conf"]