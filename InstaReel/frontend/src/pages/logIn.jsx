import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import axios from 'axios';
import 'react-toastify/dist/ReactToastify.css';

const LogIn = ({ setUserName }) => {
  console.log("you are in Login");
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    email: '',
    password: '',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(import.meta.env.VITE_SERVER_URL + "/user/login", formData);
      toast.info(response.data.message, {
        position: "bottom-right",
        autoClose: 2000,
      });
  
      if (response.data.alert) {
        const token = response.data.data.token;
        const expirationTime = Date.now() +  24 * 60 * 60 * 1000; // 2 hours in milliseconds
        localStorage.setItem('userData', JSON.stringify(response.data.data));
        localStorage.setItem('token', token);
        localStorage.setItem('tokenExpiration', expirationTime); // Save expiration time
        setUserName(response.data.data.userName);
        navigate("/");
      }
    } catch (error) {
      console.log("Error occurred:", error);
    }
  };
  

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-900">
      <div className="bg-gray-800 p-8 rounded-lg shadow-lg w-full max-w-md">
        <h1 className="text-2xl text-white mb-4 text-center">Log In</h1>
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label className="block text-gray-400 text-sm mb-2" htmlFor="email">Email</label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              className="w-full p-2 bg-gray-700 text-gray-300 rounded-lg border border-gray-600"
            />
          </div>
          <div className="mb-4">
            <label className="block text-gray-400 text-sm mb-2" htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              className="w-full p-2 bg-gray-700 text-gray-300 rounded-lg border border-gray-600"
            />
          </div>
          <button type="submit" className="w-full p-2 bg-red-600 text-white rounded-lg">Log In</button>
        </form>
        <div className="flex items-center justify-center mt-6">
          <div className="border-t border-gray-400 w-1/3"></div>
          <div className="text-gray-400 mx-2">OR</div>
          <div className="border-t border-gray-400 w-1/3"></div>
        </div>
        <div className="mt-4">
          <Link to="/signup" className="w-full p-2 bg-red-600 text-white rounded-lg block text-center">Sign Up</Link>
        </div>
      </div>
    </div>
  );
};

export default LogIn;

