import React, { useEffect, useState } from "react";
import PlaylistContainer from "./subcomponents/PlaylistContainer";
import globalVar from "../global.js";

const DatabaseMiddle = ({ setCurrentBottomSong }) => {
  const [songs, setSongs] = useState([]);

  useEffect(() => {
    const fetchSongs = async () => {
      try {
        const response = await fetch(
          "http://127.0.0.1:8008/" + globalVar.username + "/all_songs"
        );
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        const data = await response.json();
        console.log("data", data);
        const formattedSongs = data.songs.map((song) => ({
          songName: song.song_name,
          artistName: song.artist_name,
          songLength: song.duration,
          releaseYear: song.release_date,
          rating: song.rate,
          id: song.song_id,

          // include other attributes if needed
        }));

        setSongs(formattedSongs);
      } catch (error) {
        console.error("Fetch error:", error);
      }
    };

    fetchSongs();
  }, []);

  return (
    <div className="playlist-middle">
      <h1>Database</h1>
      <PlaylistContainer
        className="playlist-container"
        songs={songs}
        setCurrentBottomSong={setCurrentBottomSong}
      />
    </div>
  );
};

export default DatabaseMiddle;
