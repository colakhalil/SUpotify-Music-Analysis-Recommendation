import React from "react";

const SongDetails = ({ song }) => {
  return (
    <div className="song-info">
      <img
        src={song.thumbnail}
        alt={`${song.title} album cover`}
        className="album-cover"
      />
      <div className="firstInfo">
        <p className="song-title">{song.title}</p>
        <p className="song-artist">{song.artists}</p>
      </div>
      <div className="secondInfo">
        <p className="song-meta">Genre: {song.genre}</p>
      </div>
    </div>
  );
};

export default SongDetails;
