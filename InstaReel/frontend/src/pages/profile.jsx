import { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from "axios";

const Profile = ({ userName, setUserName }) => {
  const navigate = useNavigate();
  const [userVideos, setUserVideos] = useState([]);

  const fetchData = async () => {
    try {
          const Token = localStorage.getItem('token');
      const resp = await axios.post(import.meta.env.VITE_SERVER_URL + "/shortVideos/getUserVideos", { userName }, {
        headers: {
          Authorization: `Bearer ${Token}` 
        }
      });
      setUserVideos(resp.data); 

    } catch (error) {
      console.error("Error fetching user videos:", error);
    }
  };

  useEffect(() => {
    if (userName) {
      fetchData();
    }
  }, [userName]); 

  console.log("userVideos", userVideos);


  return (
    <div className="min-h-screen bg-gray-900 text-white ">
      
      {/* Main Content */}
      <main className="pt-20 pl-4 md:pl-60">
        <h1 className="text-2xl font-bold mb-4">Your Videos</h1>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {userVideos.length === 0 ? (
            <p>No videos available</p>
          ) : (
            userVideos.map((video) => (
              <div key={video._id} className="bg-gray-800 p-4 rounded-lg">
                <video src={video.url} controls className="w-full h-48 object-cover rounded-lg mb-2"></video>
                <p className="text-sm mb-2">{video.description}</p>
                <div className="flex justify-between items-center text-sm text-gray-400">
                  <span>Likes: {video.likes}</span>
                  <span>Comments: {video.comments.length}</span>
                </div>
              </div>
            ))
          )}
        </div>
      </main>
    </div>
  );
};

export default Profile;





