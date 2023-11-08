import React from 'react';

const SongDetails = ({ song }) => {
  return (
    <div className="song-info">
      <img src={song.img} alt={`${song.title} album cover`} className="album-cover" />
      <div className="firstInfo">
        <p className="song-title">{song.title}</p>
        <p className="song-artist">{song.artist}</p>
      </div>
      <div className="secondInfo">
        <p className="song-meta">Genre: {song.genre}</p>
        <p className="song-meta">Mood: {song.mood}</p>
        <p className="song-meta">Recording: {song.recordingType}</p>
      </div>
    </div>
  );
};

export default SongDetails;
