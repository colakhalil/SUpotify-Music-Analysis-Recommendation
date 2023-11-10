import React from 'react';
import SongRating from './SongRating';

const SongControls = ({
  isPlaying,
  togglePlay,
  currentTime,
  songDurationInSeconds,
  song,
  toggleLyrics,
  userRating,
  handleRatingChange
}) => {
  return (
    <div className="song-controls-container"> {/* Container for all song controls and extras */}
      <div className="song-controls"> {/* Container for the main controls */}
        <button className="song-lyrics-btn" onClick={toggleLyrics}>
          Lyrics
        </button>
        <button className="play-btn" onClick={togglePlay}>
          {isPlaying ? "Pause" : "Play"}
        </button>
        <input
          type="range"
          min="0"
          max={songDurationInSeconds}
          value={currentTime}
          className="slider"
          readOnly
        />
        <div className="song-timer">
          {Math.floor(currentTime / 60)}:{String(currentTime % 60).padStart(2, "0")} / {song.duration}
        </div>
      </div>
      <div className='song-rating-container'>
      <SongRating userRating={userRating} handleRatingChange={handleRatingChange} /> {/* Rating stars */}
      </div>    
    </div>
  );
};

export default SongControls;
