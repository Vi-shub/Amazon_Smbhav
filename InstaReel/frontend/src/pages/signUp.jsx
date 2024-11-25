import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import axios from 'axios';
import 'react-toastify/dist/ReactToastify.css';

const SignUp = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    userName: '',
    email: '',
    password: '',
    confirmPassword: ''
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (formData.userName && formData.confirmPassword && formData.password && formData.email) {
      if (formData.password === formData.confirmPassword) {
        await axios.post(
          import.meta.env.VITE_SERVER_URL + '/user/signup',
          formData
        )
          .then((response) => {
            if(response.data.alert){
              toast.success(response.data.message, {
                position: "bottom-right",
                autoClose: 2000,
              });
            navigate("/login");
            }
            else{
              toast.error(response.data.message, {
                position: "bottom-right",
                autoClose: 5000,
              });
            }
          })
          .catch((error) => {
            console.log("Error occurred:", error)
          })
      } else {
        toast.error("Password and Confirm Password do not match", {
          position: "bottom-right",
        });
      }
    } else {
      toast.error("Please enter required fields", {
        position: "bottom-right",
      });
    }
  };

  return (
    <>
      <div className="min-h-screen flex items-center justify-center bg-gray-900">
        <div className="bg-gray-800 p-8 rounded-lg shadow-lg w-full max-w-md">
          <h1 className="text-2xl text-white mb-4 text-center">Sign Up</h1>
          <form onSubmit={handleSubmit}>
            <div className="mb-4">
              <label className="block text-gray-400 text-sm mb-2" htmlFor="userName">User Name</label>
              <input
                type="text"
                id="userName"
                name="userName"
                value={formData.userName}
                onChange={handleChange}
                className="w-full p-2 bg-gray-700 text-gray-300 rounded-lg border border-gray-600"
              />
            </div>
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
            <div className="mb-4">
              <label className="block text-gray-400 text-sm mb-2" htmlFor="confirmPassword">Confirm Password</label>
              <input
                type="password"
                id="confirmPassword"
                name="confirmPassword"
                value={formData.confirmPassword}
                onChange={handleChange}
                className="w-full p-2 bg-gray-700 text-gray-300 rounded-lg border border-gray-600"
              />
            </div>
            <button type="submit" className="w-full p-2 bg-red-600 text-white rounded-lg">Create Account</button>
          </form>
          <div className="flex items-center justify-center mt-6">
            <div className="border-t border-gray-400 w-1/3"></div>
            <div className="text-gray-400 mx-2">OR</div>
            <div className="border-t border-gray-400 w-1/3"></div>
          </div>
          <div className="mt-4">
            <Link to="/login" className="w-full p-2 bg-red-600 text-white rounded-lg block text-center">Log In</Link>
          </div>
        </div>
      </div>
    </>
  );
};

export default SignUp;
