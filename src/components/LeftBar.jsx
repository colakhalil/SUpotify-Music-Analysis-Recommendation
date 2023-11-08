import React from 'react';
import NavigationButtons from './subcomponents/NavigationButtons';
import PlaylistCardLeftbar from './subcomponents/PlaylistCardLeftbar';

const LeftBar = ({ playlists }) => {

  const handleClick = (playlistName) => {
    console.log(`You clicked on ${playlistName}`);
    // Implement your playlist click functionality here
  };

  const handleMain = () => {
    console.log("Home clicked");
    // Implement your home click functionality here
  };

  const handleSearch = () => {
    console.log("Search clicked");
    // Implement your search click functionality here
  };

  return (
    <div className="left-bar">
      <NavigationButtons onHomeClick={handleMain} onSearchClick={handleSearch} />
      <PlaylistCardLeftbar playlists={playlists} onPlaylistClick={handleClick} />
    </div>
  );
};

export default LeftBar;
