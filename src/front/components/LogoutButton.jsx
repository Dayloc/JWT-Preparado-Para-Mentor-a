import React from 'react';
import { useNavigate } from 'react-router-dom';

function LogoutButton() {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('token');  // Elimina el token
    navigate('/login');               // Redirige al login
  };

  return (
    <button className="btn btn-danger m-5" onClick={handleLogout}>
      Cerrar sesión
    </button>
  );
}

export default LogoutButton;
