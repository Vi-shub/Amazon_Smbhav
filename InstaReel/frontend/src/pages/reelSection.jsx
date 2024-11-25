import axios from "axios";
import { useState, useEffect } from "react";
import PropTypes from 'prop-types';

const backendUrl = import.meta.env.VITE_SERVER_URL;
const recommendationUrl = 'https://recommendation-server-rzj2.onrender.com/recommend';

import VideoList from "../components/videoList";

const ReelSection = ({ userName }) => {
  const [data, setData] = useState([]);

  const fetchData = async () => {
    try {
      // Make all API requests in parallel
      const [videoResponse, interactionResponse, recommendationResponse] = await Promise.all([
        axios.get(`${backendUrl}/shortVideos/getAllVideos`),
        axios.get(`${backendUrl}/interaction/getInteractionData`, { params: { userName } }),
        axios.post(recommendationUrl, { userName })
      ]);

      const allVideos = videoResponse.data;
      const interactionData = interactionResponse.data;
      const recommendedIds = recommendationResponse.data.recommendations || [];

      // Filter out videos the user has already interacted with
      const interactedVideoIds = interactionData.map(interaction => interaction.videoId);
      const uniqueRecommendedIds = recommendedIds.filter(id => !interactedVideoIds.includes(id));

      // Create a map of all videos by their ID for easy lookup
      const videoMap = allVideos.reduce((map, video) => {
        map[video._id] = video;
        return map;
      }, {});

      // Get the video objects for the recommended IDs
      const recommendedVideos = uniqueRecommendedIds.map(id => videoMap[id]).filter(video => video);

      // Get the remaining videos
      const remainingVideos = allVideos.filter(video => !uniqueRecommendedIds.includes(video._id));

      // Combine recommended videos and the remaining videos
      let finalVideoData;
      if (recommendedVideos.length > 0) {
        finalVideoData = [...recommendedVideos, ...remainingVideos];
      } else {
        // If no recommendations, just display all videos
        finalVideoData = allVideos;
      }

      setData(finalVideoData);
    } catch (error) {
      console.error("Error fetching data:", error);
      // In case of an error, fallback to displaying all videos
      const videoResponse = await axios.get(`${backendUrl}/shortVideos/getAllVideos`);
      setData(videoResponse.data);
    }
  };

  useEffect(() => {
    fetchData();
  }, [userName]);

  return (
    <>
      <VideoList videoData={data} userName={userName} />
    </>
  );
};

ReelSection.propTypes = {
  userName: PropTypes.string.isRequired,
};

export default ReelSection;



