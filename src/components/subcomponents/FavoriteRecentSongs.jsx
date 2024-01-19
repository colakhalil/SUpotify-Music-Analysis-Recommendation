import React, { useState, useEffect } from "react";
import styles from "../../pagesCSS/FavoriteSongs90s.css";
import globalVar from "../../global.js";
const FavoriteRecentSongs = ({userName}) => {
  const [songs, setSongs] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:8008/" + userName + "/new_songs")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((data) => {
        // Ensure the data structure matches the provided JSON format
        let favorite90sSongs = data;
        favorite90sSongs = favorite90sSongs.filter((song) => song.rate >= 3);
        const first6Items =
          favorite90sSongs.length >= 6
            ? favorite90sSongs.slice(0, 6)
            : favorite90sSongs;

        console.log(first6Items);
        const transformedData = first6Items.map((song) => {
          return {
            title: song.song_name,
            artist: song.artist_name.join(" "), // Convert the array to a string with spaces
            releaseYear: song.release_date,
          };
        });

        // Set the transformed data to your state variable (e.g., albums)
        setSongs(transformedData);
      });
  }, []);

  return (
    <div>
      <h3 style={{ color: "white" }}>Your Favorite new Released Songs</h3>
      <ul className="albumsList">
        {songs.map((song) => (
          <li key={song.title} className="albumCard">
            <p className="albumTitle">{song.title}</p>
            <p className="albumArtistYear">
              {song.artist} <br />
              {song.releaseYear}
            </p>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default FavoriteRecentSongs;
