import { useState } from 'react';
import axios from 'axios';
import { toast } from 'react-toastify';

const Upload = ({userName}) => {
  
  const [formData, setFormData] = useState({ video: null, description: "", song: "", userName:userName });
  const [send, setSend]=useState(true);
  const handleChange = (e) => {
    const { name, value, files } = e.target;
    if (name === 'video') {
      setFormData({ ...formData, video: files[0] });
    } else {
      setFormData({ ...formData, [name]: value });
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!formData.video) {
      toast.error('Please select a video to upload');
      return;
    }
      console.log("formD", formData);
    const uploadData = new FormData();
    uploadData.append('video', formData.video);
    uploadData.append('description', formData.description);
    uploadData.append('song', formData.song);
    uploadData.append('userName', formData.userName);
     
        
    try {
        setSend((s)=>!s);
      const response = await axios.post(import.meta.env.VITE_SERVER_URL + '/shortVideos/upload', uploadData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
       for (let pair of uploadData.entries()) {
    console.log(pair[0]+ ', ' + pair[1]);
  }
      setSend((s)=>!s);
      toast.success('Video uploaded successfully');
    } catch (error) {
      setSend((s)=>!s);
      toast.error('Failed to upload video');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-900">
      <div className="bg-gray-800 p-8 rounded-lg shadow-lg w-full max-w-md">
        <h2 className="text-2xl text-white mb-4">Video Uploader</h2>
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label className="block text-gray-400 text-sm mb-2" htmlFor="video">Choose File</label>
            <input type="file" accept="video/*" name="video" onChange={handleChange} className="w-full text-gray-300 bg-gray-700 rounded-lg border border-gray-600 cursor-pointer" />
            {formData.video && <p className="text-gray-400 mt-2">Video uploaded successfully</p>}
          </div>
          <div className="mb-4">
            <label className="block text-gray-400 text-sm mb-2" htmlFor="description">Video Description</label>
            <input type="text" placeholder="Description" name="description" value={formData.description} onChange={handleChange} className="w-full p-2 bg-gray-700 text-gray-300 rounded-lg border border-gray-600" />
          </div>
          <div className="mb-4">
            <label className="block text-gray-400 text-sm mb-2" htmlFor="song">Song</label>
            <input type="text" placeholder="Song" name="song" value={formData.song} onChange={handleChange} className="w-full p-2 bg-gray-700 text-gray-300 rounded-lg border border-gray-600" />
          </div>
          {(send)?(<button type="submit" className="w-full p-2 bg-red-600 text-white rounded-lg">Upload</button>)
          :(<button type="submit" disabled className=" animate-pulse w-full p-2 bg-red-500 text-white rounded-lg">Uploading...</button>)}
        </form>
      </div>
    </div>
  );
};

export default Upload;




