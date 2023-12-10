import React from "react";
const Playlist = ({ name, playlistData, thumbnail, onClick }) => {
  return (
    <div className="Playlist" onClick={onClick}>
      <img
        src={thumbnail}
        alt={`${name} cover`}
        className="recommended-thumbnail"
      />
      <div className="recommended-name">{name}</div>
    </div>
  );
};
export default Playlist;
