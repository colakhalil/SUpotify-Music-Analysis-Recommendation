import React, { useState, useEffect } from "react";
import axios from "axios";
import NavigationButtons from "./subcomponents/NavigationButtons";
import PlaylistCardLeftbar from "./subcomponents/PlaylistCardLeftbar";

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

  const handleClick = (playlistName) => {
    console.log(`You clicked on ${playlistName}`);
    setCurrentPlace("playlist");
    // Implement your playlist click functionality here
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
