import React from 'react';

const PlaylistContainer = ({ songs }) => {
  return (
    <div className="playlist-container">
      {songs.map((song, index) => (
        <div className="song-row" key={index}>
          <div className="song-index">{index + 1}</div>
          <div className="song-info">
            <span className="song-name">{song.songName}</span>
            <span className="song-artist">{song.artistName}</span> {/* Fixed property name */}
          </div>
          <div className="song-duration">{song.songLength} ms</div> {/* Display song length */}
          <div className="song-rating">{song.rating}</div> {/* Display song rating */}
        </div>
      ))}
    </div>
  );
};

export default PlaylistContainer;
