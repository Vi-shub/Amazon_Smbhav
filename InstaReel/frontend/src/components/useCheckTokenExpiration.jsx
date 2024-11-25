import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';  // Import toast
import 'react-toastify/dist/ReactToastify.css';  // Import toast styles

const useCheckTokenExpiration = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const tokenExpiration = localStorage.getItem('tokenExpiration');
    if (tokenExpiration && Date.now() > parseInt(tokenExpiration, 10)) {
      // Token has expired, log out the user
      localStorage.removeItem('token');
      localStorage.removeItem('userData');
      localStorage.removeItem('tokenExpiration');
      
      // Show toast message instead of alert
      toast.error('Session expired, please log in again.', {
        position: 'top-right',
        autoClose: 5000,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true
      });

      navigate('/login', { replace: true });
      window.location.reload();
    }
  }, [navigate]);
};

export default useCheckTokenExpiration;


