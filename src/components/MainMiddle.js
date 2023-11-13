import React from "react";
import SearchBar from "./subcomponents/SearchBar";
import Playlist from "./subcomponents/Playlist";

const MainMiddle = ({ lastPlaylists, recomendedPlaylists }) => {
  const handleSearch = (searchTerm) => {
    console.log(`Search term submitted: ${searchTerm}`);
    // You can now do something with the search term,
    // like making an API call to fetch search results
  };
  const handlePlaylistClick = (playlistName) => {
    console.log(`Playlist clicked: ${playlistName}`);
    // Here you would handle the click event, such as navigating to the playlist page.
  };
  // when song is updated this BottomBar also will be updated automatically

  return (
    <div className="content-container">
      <SearchBar onSearch={handleSearch} />
      <h2 className="last-played-title">Your last played Playlists </h2>
      <div className="lastPlaylists-container">
        {lastPlaylists.map((lastPlaylists, index) => (
          <Playlist
            key={index}
            name={lastPlaylists.name}
            thumbnail={lastPlaylists.thumbnail}
            onClick={() => handlePlaylistClick(lastPlaylists.name)}
          />
        ))}
      </div>
      <h2 className="recommended-playlists">Recomended Playlists</h2>
      <div className="recomended-playlists-container">
        {recomendedPlaylists.map((recomendedPlaylists, index) => (
          <Playlist
            key={index}
            name={recomendedPlaylists.name}
            thumbnail={recomendedPlaylists.thumbnail}
            onClick={() => handlePlaylistClick(recomendedPlaylists.name)}
          />
        ))}
      </div>
    </div>
  );
};

export default MainMiddle;
