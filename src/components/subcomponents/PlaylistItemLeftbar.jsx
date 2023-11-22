import React from "react";

const PlaylistItemLeftbar = ({ playlist, onClick }) => {
  return (
    <button
      className="playlist-button"
      onClick={() => onClick(playlist.playlistID)}
    >
      <img
        src={playlist.playlistPic}
        alt={playlist.name}
        className="playlist-image"
      />
      <div className="playlist-info">
        <div className="playlist-name">{playlist.name}</div>
        <div className="song-number">{playlist.songNumber} songs</div>
      </div>
    </button>
  );
};

export default PlaylistItemLeftbar;
