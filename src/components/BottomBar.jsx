import React, { useState, useEffect } from 'react';
import SongDetails from './subcomponents/SongDetails';
import SongControls from './subcomponents/SongControls';
import SongRating from './subcomponents/SongRating';
import SongOptions from './subcomponents/SongOptions';
import SongDetailsExtra from './subcomponents/SongDetailsExtra';

const BottomBar = ({ song }) => {
  const [userRating, setUserRating] = useState(song.userPrevRating);
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);

  const handleRatingChange = (newRating) => {
    setUserRating(newRating);
    console.log("NEW RATING: ", newRating);
    // Add additional logic for when the rating changes
  };

  const togglePlay = () => {
    setIsPlaying(!isPlaying);
    // Add additional logic for when play/pause is toggled
  };

  const toggleLyrics = () => {
    console.log("Lyrics toggled");
    // Add additional logic for when lyrics are toggled
  };

  const getSecondsFromDuration = (duration) => {
    const [minutes, seconds] = duration.split(":").map(Number);
    return minutes * 60 + seconds;
  };

  const songDurationInSeconds = getSecondsFromDuration(song.duration);

  useEffect(() => {
    let interval;
    if (isPlaying) {
      interval = setInterval(() => {
        setCurrentTime((currentTime) => {
          const newTime = currentTime + 1;
          if (newTime >= songDurationInSeconds) {
            setIsPlaying(false);
            return songDurationInSeconds;
          }
          return newTime;
        });
      }, 1000);
    }
    return () => clearInterval(interval);
  }, [isPlaying, songDurationInSeconds]);

  useEffect(() => {
    if (currentTime >= songDurationInSeconds) {
      setIsPlaying(false);
      setCurrentTime(0);
    }
  }, [currentTime, songDurationInSeconds]);

  return (
    <div className="song-bar">
      <SongDetails song={song} />
      <SongControls
        isPlaying={isPlaying}
        togglePlay={togglePlay}
        currentTime={currentTime}
        songDurationInSeconds={songDurationInSeconds}
        song={song}
        toggleLyrics={toggleLyrics}
        userRating={userRating}
         handleRatingChange={handleRatingChange}
      />
      <SongDetailsExtra song={song}/>
    </div>
  );
};

export default BottomBar;
