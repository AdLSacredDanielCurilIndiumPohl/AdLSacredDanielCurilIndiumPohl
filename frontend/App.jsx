import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';

const DatabaseCard = ({ name, status, onConnect }) => (
  <motion.div
    whileHover={{ scale: 1.05 }}
    className="bg-white p-6 rounded-lg shadow-lg"
  >
    <h3 className="text-xl font-bold mb-2">{name}</h3>
    <div className={`h-3 w-3 rounded-full inline-block mr-2 ${
      status === 'connected' ? 'bg-green-500' : 'bg-gray-300'
    }`} />
    <span className="text-gray-600">{status}</span>
    <button
      onClick={() => onConnect(name)}
      className="mt-4 bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
    >
      Verbinden
    </button>
  </motion.div>
);

const App = () => {
  const [databases, setDatabases] = useState({
    PostgreSQL: 'disconnected',
    MongoDB: 'disconnected',
    Redis: 'disconnected',
    Neo4j: 'disconnected'
  });

  const [clusterStatus, setClusterStatus] = useState('inactive');

  const connectDatabase = async (name) => {
    try {
      const response = await fetch(`/api/connect/${name.toLowerCase()}`);
      const data = await response.json();
      
      setDatabases(prev => ({
        ...prev,
        [name]: data.status
      }));
    } catch (error) {
      console.error(`Fehler beim Verbinden mit ${name}:`, error);
    }
  };

  const triggerConnectAll = async () => {
    try {
      await fetch('/api/semantic/trigger/CONNECT:ALL', { method: 'POST' });
      setClusterStatus('active');
      // Aktualisiere alle Datenbankstatus
      Object.keys(databases).forEach(db => {
        setDatabases(prev => ({
          ...prev,
          [db]: 'connected'
        }));
      });
    } catch (error) {
      console.error('Fehler beim Cluster-Connect:', error);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-4xl font-bold mb-8 text-center">
          ORDO.CONNECTORIS Dashboard
        </h1>
        
        <div className="mb-8 text-center">
          <button
            onClick={triggerConnectAll}
            className="bg-purple-600 text-white px-6 py-3 rounded-lg text-lg hover:bg-purple-700"
          >
            CONNECT:ALL Trigger
          </button>
          <div className="mt-2 text-gray-600">
            Cluster Status: 
            <span className={clusterStatus === 'active' ? 'text-green-600' : 'text-gray-600'}>
              {clusterStatus}
            </span>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {Object.entries(databases).map(([name, status]) => (
            <DatabaseCard
              key={name}
              name={name}
              status={status}
              onConnect={connectDatabase}
            />
          ))}
        </div>
      </div>
    </div>
  );
};

export default App;