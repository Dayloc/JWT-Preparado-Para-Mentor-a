import React, { useEffect, useState } from 'react';
import { Navigate } from 'react-router-dom';

function PrivateRoute({ children }) {
  const [isValid, setIsValid] = useState(null); // null = cargando
  const token = localStorage.getItem('token');

  useEffect(() => {
    const verifyToken = async () => {
      if (!token) {
        setIsValid(false);
        return;
      }

      try {
        const response = await fetch('https://redesigned-sniffle-6996j49wxrqqc5v6x-3001.app.github.dev/api/verify-token', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        setIsValid(response.ok); // si el backend devuelve 200, el token es válido
      } catch {
        setIsValid(false);
      }
    };

    verifyToken();
  }, [token]);

  if (isValid === null) return <p>Cargando...</p>;

  return isValid ? children : <Navigate to="/login" replace />;
}

export default PrivateRoute;
