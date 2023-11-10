import React from 'react';

const SongDetailsExtra = ({ song }) => {
  return (
    <div className="song-details-extra">
        <p className="song-meta">Instruments: {song.instruments}</p>
        <p className="song-meta">Plays: {song.playCount}</p>
        <p className="song-meta">Release: {song.releaseYear}</p>
        <p className="song-meta">Added: {song.dateAdded}</p>
    </div>
  );
};

export default SongDetailsExtra;

