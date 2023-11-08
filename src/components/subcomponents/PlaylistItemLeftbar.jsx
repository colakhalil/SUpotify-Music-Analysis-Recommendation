import React from 'react';

const PlaylistItemLeftbar = ({ playlist, onClick }) => {
  return (
    <button
      className="playlist-button"
      onClick={() => onClick(playlist.playlist_name)}
    >
      <img
        src={playlist.playlist_picture}
        alt={playlist.playlist_name}
        className="playlist-image"
      />
      <div className="playlist-info">
        <div className="playlist-name">{playlist.playlist_name}</div>
        <div className="song-number">{playlist.song_number} songs</div>
      </div>
    </button>
  );
};

export default PlaylistItemLeftbar;
