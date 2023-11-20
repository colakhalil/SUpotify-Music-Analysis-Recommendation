import React, { useState, useEffect } from "react";
import styles from "../../pagesCSS/FavoriteSongs90s.css";

const FavoriteAlbums90s = () => {
  const [albums, setAlbums] = useState([]);

  useEffect(() => {
    // Correct path assuming your server setup serves the public directory
    fetch("../../../data/albums.json")
      .then((response) => response.json())
      .then((data) => {
        const favorite90sAlbums = data
          .filter(
            (album) => album.releaseYear >= 1990 && album.releaseYear < 2000
          )
          .slice(0, 10);
        setAlbums(favorite90sAlbums);
      });
  }, []);

  return (
    <div>
      <h3 style={{ color: "white" }}>Your Favorite 10 '90s Albums</h3>
      <ul className="albumsList">
        {albums.map((album) => (
          <li key={album.title} className="albumCard">
            <p className="albumTitle">{album.title}</p>
            <p className="albumArtistYear">
              {album.artist} <br />
              {album.releaseYear}
            </p>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default FavoriteAlbums90s;
