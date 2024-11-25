import { useRef, useState, useEffect } from "react";
import Footer from "./footer";
import VideoSideBar from "./VideoSideBar";
import axios from "axios";
import { FaPlayCircle, FaVolumeUp, FaVolumeMute } from 'react-icons/fa';

const Video = ({ item, userName }) => {
    const [playing, setPlaying] = useState(false);
    const [muted, setMuted] = useState(false);
    const videoRef = useRef(null);
    const [isVisible, setIsVisible] = useState(false);
    const [hasViewed, setHasViewed] = useState(false);
    const [showPlayIcon, setShowPlayIcon] = useState(true);

    const video = item.url;

    useEffect(() => {
        const options = {
            root: null,
            rootMargin: '0px',
            threshold: 0.5
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                setIsVisible(entry.isIntersecting);
            });
        }, options);

        if (videoRef.current) {
            observer.observe(videoRef.current);
        }

        return () => observer.disconnect();
    }, []);

    useEffect(() => {
        if (isVisible && videoRef.current) {
            attemptAutoplay();
        } else if (videoRef.current) {
            videoRef.current.pause();
            setPlaying(false);
            setShowPlayIcon(true);
        }
    }, [isVisible]);

    const attemptAutoplay = async () => {
        try {
            await videoRef.current.play();
            setPlaying(true);
            setShowPlayIcon(false);
            setMuted(false);
        } catch (error) {
            console.error("Unmuted autoplay failed:", error);
            // Fallback: try muted autoplay
            videoRef.current.muted = true;
            try {
                await videoRef.current.play();
                setPlaying(true);
                setShowPlayIcon(false);
                setMuted(true);
            } catch (mutedError) {
                console.error("Muted autoplay also failed:", mutedError);
                setPlaying(false);
                setShowPlayIcon(true);
            }
        }
    };

    const handleVideoPress = () => {
        if (videoRef.current) {
            if (playing) {
                videoRef.current.pause();
                setPlaying(false);
                setShowPlayIcon(true);
            } else {
                videoRef.current.play().catch(console.error);
                setPlaying(true);
                setShowPlayIcon(false);
            }
        }
    };

    const toggleMute = () => {
        if (videoRef.current) {
            videoRef.current.muted = !videoRef.current.muted;
            setMuted(videoRef.current.muted);
        }
    };

    const handleVideoProgress = () => {
        const videoElement = videoRef.current;
        if (videoElement) {
            const percentWatched = (videoElement.currentTime / videoElement.duration) * 100;

            if (percentWatched >= 50 && !hasViewed) {
                setHasViewed(true);
                axios.post(`${import.meta.env.VITE_SERVER_URL}/interaction/postInteractionData`, {
                    userName,
                    videoId: item._id,
                    interactionType: 'view'
                })
                    .then(response => {
                        console.log("View registered successfully:", response.data);
                    })
                    .catch(error => {
                        console.error("Error registering view:", error);
                    });
            }
        }
    };

    return (
        <>
            <div className="relative h-[600px] w-[350px] flex items-center justify-center snap-start snap-always m-8">
                <video
                    src={video}
                    loop
                    ref={videoRef}
                    onClick={handleVideoPress}
                    onTimeUpdate={handleVideoProgress}
                    className=" rounded-xl h-[600px] bg-black"
                    playsInline
                />
                {showPlayIcon && (
                    <FaPlayCircle
                        className="absolute text-white text-6xl opacity-80 cursor-pointer"
                        style={{ top: '50%', left: '50%', transform: 'translate(-50%, -50%)' }}
                        onClick={handleVideoPress}
                    />
                )}
                <div 
                    className="absolute top-3 right-3 text-white text-2xl cursor-pointer"
                    onClick={toggleMute}
                >
                    {muted ? <FaVolumeMute /> : <FaVolumeUp />}
                </div>
                <div className="absolute bottom-3 left-3">
                    <Footer userName={item.userName} description={item.description} song={item.song} />
                </div>
                <VideoSideBar item={item} userName={userName} />
            </div>
        </>
    );
};

export default Video;

