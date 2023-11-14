import React from 'react';

const PlaylistContainer = ({ songs }) => {
  return (
    <div className="playlist-container">
      {songs.map((song, index) => (
        <div className="song-row" key={index}>
          <div className="song-index">{index + 1}</div>
          <div className="song-info">
            <span className="song-name">{song.songName}</span>
            <span className="song-artist">{song.artist}</span>
          </div>
          <div className="song-duration">{song.duration}</div>
          <div className="song-rating">{song.songRating}</div>
        </div>
      ))}
    </div>
  );
};

export default PlaylistContainer;
