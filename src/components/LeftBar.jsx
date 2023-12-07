import React, { useState, useEffect } from "react";
import axios from "axios";
import NavigationButtons from "./subcomponents/NavigationButtons";
import PlaylistCardLeftbar from "./subcomponents/PlaylistCardLeftbar";
import globalVar from "../global";

const LeftBar = ({ setCurrentPlace, setCurrentPlaylistInfo }) => {
  const [playlists, setPlaylists] = useState([]);

  useEffect(() => {
    // Fetch playlists from the API when the component mounts
    const fetchPlaylists = async () => {
      try {
        const response = await axios.get(
          "http://127.0.0.1:8008/get_user_playlists"
        );
        setPlaylists(response.data); // Update the state with the fetched playlists
      } catch (error) {
        console.error("Error fetching playlists:", error);
      }
    };

    fetchPlaylists();
  }, []);

  function transformJson(originalJson) {
    return {
      album: originalJson.artist + " Album", // You might need a better way to determine the album name
      artistName: originalJson.artist,
      rating: originalJson.song_rating,
      releaseYear: originalJson.release_year.split("-")[0],
      songLength: originalJson.duration,
      songName: originalJson.song_name, // Placeholder, replace with actual logic to determine the picture URL
    };
  }
  function transformPlaylistJson(originalJson) {
    return {
      ...originalJson, // Spread the rest of the original object properties
      name: originalJson.playlistName, // Rename playlistName to name
      url: originalJson.playlistPicture, // Rename playlistPicture to imageUrl
      // Remove the old properties if you no longer need them
    };
  }

  const handleClick = async (playlistId) => {
    console.log(`You clicked on playlist with ID: ${playlistId}`);

    const url =
      "http://127.0.0.1:8008/get_playlist_info/" +
      globalVar.username +
      "/" +
      playlistId;

    try {
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      let data = await response.json(); // Parsing the JSON data
      console.log("Fetched data in leftbar: ", data); // Now you log the actual data

      // Assuming transformJson is a function that transforms each song
      // For example:
      // function transformJson(song) {
      //   // transform logic here
      //   return transformedSong;
      // }

      const transformedArray = data.songs.map(transformJson);

      data.songs = transformedArray;
      data = transformPlaylistJson(data);
      // Update the songs array in data with the transformed array

      setCurrentPlaylistInfo(data);
      setCurrentPlace("playlist");

      /* After getting data put this data to umit's playlist component*/
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  const handleMain = () => {
    console.log("Home clicked");
    setCurrentPlace("main");
    // Implement your home click functionality here
  };

  const handleSearch = () => {
    console.log("Search clicked");
    // Implement your search click functionality here
  };

  const handleProfile = () => {
    console.log("You clicked on profile");
    setCurrentPlace("profile");
    // Implement your profile click functionality here
  };

  const handleDatabaseClick = () => {
    console.log("You clicked on databse");
    setCurrentPlace("database");
    // Implement your profile click functionality here
  };

  return (
    <div className="left-bar">
      <NavigationButtons
        onHomeClick={handleMain}
        onSearchClick={handleSearch}
        onProfileClick={handleProfile}
        onDatabaseClick= {handleDatabaseClick}
      />
      <PlaylistCardLeftbar
        playlists={playlists}
        onPlaylistClick={handleClick}
      />
    </div>
  );
};

export default LeftBar;
