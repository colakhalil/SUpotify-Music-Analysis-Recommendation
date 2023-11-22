import React from "react";
import PropTypes from "prop-types";

const FriendPlaylists = ({ name, thumbnail, onClick }) => {
  return (
    <div className="friend-playlist-item" onClick={onClick}>
      <img src={thumbnail} alt={`Playlist: ${name}`} className="playlist-thumbnail" />
      <p className="playlist-name">{name}</p>
    </div>
  );
};

FriendPlaylists.propTypes = {
  name: PropTypes.string.isRequired,
  thumbnail: PropTypes.string.isRequired,
  onClick: PropTypes.func.isRequired,
};

export default FriendPlaylists;
