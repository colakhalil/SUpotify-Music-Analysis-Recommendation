import React from 'react';

const SongControls = ({ isPlaying, togglePlay, currentTime, songDurationInSeconds, song }) => {
  return (
    <div className="song-controls">
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
  );
}
  export default SongControls;
