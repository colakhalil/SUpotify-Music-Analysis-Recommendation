import React from "react";
import PropTypes from "prop-types";

const FriendPart = ({ friendData }) => {
  const { name, profilePicture, favoriteGenre, bio } = friendData;

  return (
    <div className="friend-part-container">
      <img src={profilePicture} alt={`${name}'s profile`} className="friend-profile-picture"/>
      <div className="friend-info">
        <h1 className="friend-name">{name}</h1>
        <p className="friend-favorite-genre">Favorite Genre: {favoriteGenre}</p>
        <p className="friend-bio">{bio}</p>
      </div>
    </div>
  );
};

FriendPart.propTypes = {
  friendData: PropTypes.shape({
    name: PropTypes.string.isRequired,
    profilePicture: PropTypes.string.isRequired,
    favoriteGenre: PropTypes.string,
    bio: PropTypes.string,
  }).isRequired,
};

export default FriendPart;
