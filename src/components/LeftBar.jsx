import React from "react";
import NavigationButtons from "./subcomponents/NavigationButtons";
import PlaylistCardLeftbar from "./subcomponents/PlaylistCardLeftbar";

const LeftBar = ({ playlists, setCurrentPlace }) => {
  const handleClick = (playlistName) => {
    console.log(`You clicked on ${playlistName}`);
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

  const handleProfile = (playlistName) => {
    console.log("You clicked on profile");
    setCurrentPlace("profile");
    // Implement your playlist click functionality here
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
