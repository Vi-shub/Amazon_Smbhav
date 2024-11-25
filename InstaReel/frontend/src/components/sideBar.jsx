
import { UserCircle, LogOut, Home, PlusCircle, Search } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const Sidebar = ({ userName, setUserName}) => {
    const navigate = useNavigate();
    const onLogout = () => {
        localStorage.removeItem('userData');
        localStorage.removeItem('token');
        setUserName(''); 
        navigate('/login');
      };
  return (
    <div className="fixed left-6 top-20 bottom-0 w-48 bg-gray-800 flex flex-col items-start justify-between py-4 px-2  rounded-lg border-gray-600 border-[1px] hidden md:flex">
      <div className="flex flex-col items-start space-y-6 w-full">
        <button className="text-white hover:text-gray-300 flex items-center space-x-2 w-full" title="Home" onClick={() => navigate('/')}>
          <Home size={24} />
          <span>Home</span>
        </button>
        <button className="text-white hover:text-gray-300 flex items-center space-x-2 w-full" title="Search">
          <Search size={24} />
          <span>Search</span>
        </button>
        <button className="text-white hover:text-gray-300 flex items-center space-x-2 w-full" title="Create">
          <PlusCircle size={24} />
          <span>Create</span>
        </button>
      </div>
      <div className="flex flex-col items-start space-y-6 w-full">
        <button className="text-white hover:text-gray-300 flex items-center space-x-2 w-full" title={`Profile: ${userName}`} onClick={() => navigate('/profile')}>
          <UserCircle size={24} />
          <span>Profile</span>
        </button>
        <button className="text-white hover:text-gray-300 flex items-center space-x-2 w-full" onClick={onLogout} title="Logout">
          <LogOut size={24} />
          <span>Logout</span>
        </button>
      </div>
    </div>
  );
};

export default Sidebar;