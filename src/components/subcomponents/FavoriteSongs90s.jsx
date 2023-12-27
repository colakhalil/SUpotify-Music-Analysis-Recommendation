import React, { useState, useEffect } from "react";
import styles from "../../pagesCSS/FavoriteSongs90s.css";
import globalVar from "../../global.js";

const FavoriteAlbums90s = (userName) => {
  const [albums, setAlbums] = useState([]);

  useEffect(() => {
    // Correct path assuming your server setup serves the public directory

    fetch("http://127.0.0.1:8008/" + userName + "/90s")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((data) => {
        // Ensure the data structure matches the provided JSON format
        const favorite90sSongs = data;

        // Transform the data into the desired format
        const transformedData = favorite90sSongs.highly_rated_90s_songs.map(
          (song) => {
            return {
              title: song.title,
              artist: song.artist.join(" "), // Convert the array to a string with spaces
              releaseYear: song.releaseYear,
            };
          }
        );
        const first6Items =
          transformedData.length >= 6
            ? transformedData.slice(0, 6)
            : transformedData;
        // Set the transformed data to your state variable (e.g., albums)
        setAlbums(first6Items);
      });
  }, []);

  return (
    <div>
      <h3 style={{ color: "white" }}>Your Favorite 90s Songs</h3>
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
