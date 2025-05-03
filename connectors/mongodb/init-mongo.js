// Erstelle Admin-Benutzer für das Cluster
db.createUser({
    user: process.env.MONGO_INITDB_ROOT_USERNAME,
    pwd: process.env.MONGO_INITDB_ROOT_PASSWORD,
    roles: ["root"]
});

// Initialisiere die Hauptdatenbank
db = db.getSiblingDB(process.env.MONGO_INITDB_DATABASE);

// Erstelle initiale Collections
db.createCollection("cluster_metadata");
db.cluster_metadata.insertOne({
    clusterId: "ordo_connectoris_cluster",
    created: new Date(),
    status: "initialized"
});

// Aktiviere Sharding für die Datenbank
sh.enableSharding(process.env.MONGO_INITDB_DATABASE);