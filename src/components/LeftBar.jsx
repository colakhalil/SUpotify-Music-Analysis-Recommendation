import React, { useState, useEffect } from "react";
import axios from "axios";
import NavigationButtons from "./subcomponents/NavigationButtons";
import PlaylistCardLeftbar from "./subcomponents/PlaylistCardLeftbar";
import globalVar  from "../global";

const LeftBar = ({ setCurrentPlace }) => {
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

  const handleClick = async (playlistId) => {
    console.log("You clicked on playlist with ID: " + playlistId);

    const url =
      "http://127.0.0.1:8008/get_playlist_info/" +
      globalVar.username +
      "/" +
      playlistId;

    try {
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error('HTTP error! status: ' + response.status);
      }
      const data = await response.json(); // Parsing the JSON data
      console.log("Fetched data in leftbar: ", data); // Now you log the actual data

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

  return (
    <div className="left-bar">
      <NavigationButtons
        onHomeClick={handleMain}
        onSearchClick={handleSearch}
        onProfileClick={handleProfile}
      />
      <PlaylistCardLeftbar
        playlists={playlists}
        onPlaylistClick={handleClick}
      />
    </div>
  );
};

export default LeftBar;
