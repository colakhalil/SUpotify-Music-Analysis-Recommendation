import React from "react";
import PropTypes from "prop-types";

const FavoriteArtists = ({ artists, onArtistClick }) => {
  return (
    <div className="favorite-artists-container">
      <h3 className="favorite-artists-title">Favorite Artists</h3>
      <ul className="artist-list">
        {artists.map((artist, index) => (
          <li key={index} className="artist-item" onClick={() => onArtistClick(artist.name)}>
            <img src={artist.image} alt={artist.name} className="artist-image" />
            <span className="artist-name">{artist.name}</span>
          </li>
        ))}
      </ul>
    </div>
  );
};

FavoriteArtists.propTypes = {
  artists: PropTypes.arrayOf(
    PropTypes.shape({
      name: PropTypes.string.isRequired,
      image: PropTypes.string.isRequired
    })
  ).isRequired,
  onArtistClick: PropTypes.func.isRequired,
};

export default FavoriteArtists;
