import React from "react";

const PlaylistContainer = ({ songs }) => {
  console.log(songs);
  return (
    <div className="playlist-container">
      {songs.map((song, index) => (
        <div className="song-row" key={index}>
          <div className="song-index">{index + 1}</div>
          <div className="song-info">
            <span className="song-name">{song.songName}</span>
            <span className="song-artist">{song.artistName}</span>
          </div>
          <div className="song-duration">{formatDuration(song.songLength)}</div>
          <div className="song-rating">{song.rating}</div>
        </div>
      ))}
    </div>
  );
};

// Helper function to format song duration from milliseconds to "mm:ss"
const formatDuration = (durationMs) => {
  const minutes = Math.floor(durationMs / 60000);
  const seconds = ((durationMs % 60000) / 1000).toFixed(0);
  return `${minutes}:${seconds < 10 ? "0" : ""}${seconds}`;
};

// Helper function to format song rating (e.g., out of 10)
const formatRating = (rating) => {
  return `${rating}/10`;
};

export default PlaylistContainer;
