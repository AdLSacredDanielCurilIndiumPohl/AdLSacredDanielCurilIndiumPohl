FROM neo4j:latest

# Neo4j Konfiguration
ENV NEO4J_AUTH=neo4j/\${NEO4J_PASSWORD}
ENV NEO4J_dbms_security_procedures_unrestricted=apoc.*
ENV NEO4J_dbms_security_procedures_whitelist=apoc.*
ENV NEO4J_apoc_import_file_enabled=true
ENV NEO4J_apoc_export_file_enabled=true

# APOC Plugin für erweiterte Funktionen installieren
RUN wget -P /var/lib/neo4j/plugins \
    https://github.com/neo4j-contrib/neo4j-apoc-procedures/releases/download/4.4.0.12/apoc-4.4.0.12-all.jar

# RDF-Support für semantische Abfragen
RUN wget -P /var/lib/neo4j/plugins \
    https://github.com/neo4j-labs/neosemantics/releases/download/4.4.0.2/neosemantics-4.4.0.2.jar

# Ports exponieren (Bolt, HTTP, HTTPS)
EXPOSE 7687 7474 7473

# Healthcheck konfigurieren
HEALTHCHECK --interval=30s --timeout=3s \
    CMD wget -q --no-check-certificate -O - https://localhost:7473 || exit 1

# Volume für persistente Daten
VOLUME /data