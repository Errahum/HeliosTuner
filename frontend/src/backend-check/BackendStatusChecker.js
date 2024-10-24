import React, { useEffect, useState, useCallback } from 'react';
import axios from 'axios';

const BackendStatusChecker = ({ children }) => {
  const [backendStatus, setBackendStatus] = useState(null);
  const url = process.env.REACT_APP_BACKEND_URL || 'http://localhost:5000';

  const checkBackendStatus = useCallback(async () => {
    try {
      console.log("Checking backend status..."); // Log avant la requête
      const response = await axios.get('/api/check-backend-status');
      console.log("Response received:", response); // Log de la réponse

      if (response.status === 200 || response.status === 304) {
        const data = response.status === 304 ? { status: "ok" } : response.data;
        console.log("Response data:", data); // Log des données de la réponse
        setBackendStatus(true);
      } else if (response.status === 404) {
        console.log("Endpoint not found:", response.status); // Log du statut de la réponse
        setBackendStatus(false);
        alert("Error: The endpoint /api/check-backend-status was not found on the backend. Please ensure the backend is running and the endpoint is correctly defined.");
      } else {
        console.log("Response not ok:", response.status); // Log du statut de la réponse
        setBackendStatus(false);
      }
    } catch (error) {
      console.error("Error checking backend status:", error); // Log de l'erreur
      setBackendStatus(false);
      if (error.name === 'TypeError' && error.message === 'Failed to fetch') {
        alert("Error: Failed to fetch. This could be due to network issues, the server being down, or CORS policy restrictions.");
      } else {
        alert(`Error: ${error.message}`);
      }
    }
  }, []);

  useEffect(() => {
    checkBackendStatus();
  }, [checkBackendStatus]);

  if (backendStatus === null) {
    return <div>Vérification du statut du service...</div>; // Afficher un message de chargement pendant la vérification
  }

  if (backendStatus === false) {
    return (
      <div>
        Le service n'est pas disponible. Veuillez réessayer plus tard.
        <button onClick={checkBackendStatus}>Réessayer</button>
      </div>
    );
  }

  return children;
};

export default BackendStatusChecker;