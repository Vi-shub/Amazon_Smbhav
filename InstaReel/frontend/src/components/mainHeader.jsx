import { useState } from 'react';
import { Link } from 'react-router-dom';
import LOGO from '../assets/LOGO.png';
import { FaUpload } from 'react-icons/fa';
import { IoMdContact } from 'react-icons/io';
import { toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const Header = ({ userName, setUserName }) => {


  // const handleLogout = () => {
  //   localStorage.removeItem('userData');
  //   setUserName('');
  //   toast.info('Logged out successfully', {
  //     position: "bottom-right",
  //     autoClose: 2000,
  //   });
  //   setDropDown(false); 
  // };

  return (
    <>
    <div className="h-12 md:h-16 top-1 md:top-2 fixed left-1 right-1 md:left-6 md:right-6  flex items-cente shadow-lg border-gray-600 border-[1px] bg-gray-800 rounded-lg">
      <Link to="/" className="ml-10 md:mt-2 h-10 w-10">
        <img src={LOGO} alt="Logo" className="h-full w-full" />
      </Link>
      <div className="absolute flex right-2 items-center md:mt-2">
        {userName ? (
          <Link to="/upload" className="flex m-2 text-slate-50 items-center">
            <FaUpload className="mt-1" />
            <div>Upload</div>
          </Link>
        ) : (
          <Link to="/login" className="flex m-2 text-slate-50 items-center">
            <FaUpload className="mt-1" />
            <div>Upload</div>
          </Link>
        )}

        {userName ? (
          <div className="relative">
            <div className="flex m-2 text-slate-50 items-center cursor-pointer" onClick={() => setDropDown(prev => !prev)}>
              <IoMdContact className="mt-1" />
              <Link to="/profile" className="ml-2">{userName}</Link>
            </div>
            
          </div>
        ) : (
          <Link to="/login" className="flex m-2 text-slate-50 items-center">
            <IoMdContact className="mt-1" />
            <div>Login</div>
          </Link>
        )}
      </div>
    </div>
    </>
  );
};

export default Header;






