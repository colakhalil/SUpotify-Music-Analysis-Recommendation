import React, { useState, useEffect } from "react";
import styles from "../../pagesCSS/FavoriteSongs90s.css";
const FavoriteRecentSongs = () => {
  const [songs, setSongs] = useState([]);

  useEffect(() => {
    fetch("../../../data/songs.json")
      .then((response) => response.json())
      .then((data) => {
        const sixMonthsAgo = new Date();
        sixMonthsAgo.setMonth(sixMonthsAgo.getMonth() - 6);

        const recentSongs = data.slice(0, 10);
        setSongs(recentSongs);
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
