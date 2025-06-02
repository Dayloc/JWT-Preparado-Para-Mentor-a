import React, { useEffect, useState } from 'react';
import LogoutButton from '../components/LogoutButton';

function Dashboard() {
  const [userData, setUserData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchUserData = async () => {
      const token = localStorage.getItem('token');

      try {
        const response = await fetch('https://redesigned-sniffle-6996j49wxrqqc5v6x-3001.app.github.dev/api/users', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (!response.ok) {
          throw new Error('Acceso no autorizado');
        }

        const data = await response.json();
        setUserData(data);
      } catch (err) {
        setError(err.message);
      }
    };

    fetchUserData();
  }, []);

  return (
    <div className="container mt-5">
      {/* Encabezado y botón alineados horizontalmente */}
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2 className="mb-0">Bienvenido al Dashboard</h2>
        <LogoutButton />
      </div>

      {error && (
        <div className="alert alert-danger" role="alert">
          {error}
        </div>
      )}

      {userData ? (
        <div className="card p-3 shadow-sm">
          <h5>Datos del usuario:</h5>
          <pre className="bg-light p-2 rounded">{JSON.stringify(userData, null, 2)}</pre>
        </div>
      ) : !error ? (
        <p>Cargando datos...</p>
      ) : null}
    </div>
  );
}

export default Dashboard;
