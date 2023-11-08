import React from 'react';
const Playlist = ({ name, thumbnail, onClick }) => {
  return (
    <div className="Playlist" onClick={onClick}>

      <img src={thumbnail} alt={`${name} cover`} className="lastPlaylists-thumbnail" />
      <div className="lastPlaylists-name">{name}</div>
    </div>
  );
};

export default Playlist;
