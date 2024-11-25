import { lazy, Suspense } from 'react';
const Video = lazy(() => import('./video'));
import { useState, useEffect } from "react";
import loadingImg from "../assets/image.png"
const VideoList = ({ videoData, userName }) => {
  const [videoDetail, setVideoDetail] = useState([]);
  console.log(userName);
  console.log(videoData);
  useEffect(() => {
    if (videoData) {
      setVideoDetail(videoData);
    }
  }, [videoData]);

  return (
    <Suspense fallback={<div>Loading...</div>}>
    <div className="bg-gray-900 overflow-hidden">
      <div className="relative flex flex-col items-center h-screen  overflow-scroll snap-y snap-mandatory top-14 md:top-20 md:left-28">
        {videoDetail.length > 0 ? (
          videoDetail.map((item) => <Video key={item._id} item={item} userName={userName} />)
        ) : (
          
            <div className="w-[350px] h-[600px] my-8">
              <img src={loadingImg} alt="loading video"  className="h-full w-full rounded-lg"/>
            </div>
          
        )}
      </div>
    </div>
    </Suspense>
  );
};

export default VideoList;



