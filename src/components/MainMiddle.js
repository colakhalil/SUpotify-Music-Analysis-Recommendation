import React from "react";
import SearchBar from "./subcomponents/SearchBar";
import Playlist from "./subcomponents/Playlist";

const MainMiddle = ({
  lastPlaylists,
  recomendedPlaylists,
  setCurrentPlace,
  recommendations,
  playlistPop,
  playlistRock,
  playlistJazz,
  playlistHiphop,
}) => {
  const handleSearch = (searchTerm) => {
    console.log(`Search term submitted: ${searchTerm}`);
    // You can now do something with the search term,
    // like making an API call to fetch search results
  };
  const handlePlaylistClick = (playlistName, setCurrentPlace) => {
    setCurrentPlace("playlist");
    console.log(`Playlist clicked: ${playlistName}`);
    // Here you would handle the click event, such as navigating to the playlist page.
  };
  // when song is updated this BottomBar also will be updated automatically

  return (
    <div className="content-container">
      <SearchBar onSearch={handleSearch} />
      <h2 className="recommended-title">
        Recommended Playlists Based on Genre
      </h2>
      <div className="header-line" />
      <div class="container">
        <div class="Playlist1">
          <Playlist
            name="Pop"
            playlistPop={playlistPop}
            thumbnail={
              "https://cdn.mos.cms.futurecdn.net/oCtbBypcUdNkomXw7Ryrtf-650-80.jpg.webp"
            }
            onClick={() => handlePlaylistClick("Pop", setCurrentPlace)}
          />
        </div>
        <div class="Playlist2">
          <Playlist
            name="Rock"
            playlistRock={playlistRock}
            thumbnail={
              "https://cdn.mos.cms.futurecdn.net/oCtbBypcUdNkomXw7Ryrtf-650-80.jpg.webp"
            }
            onClick={() => handlePlaylistClick("Rock", setCurrentPlace)}
          />
        </div>
        <div class="Playlist3">
          <Playlist
            name="Jazz"
            playlistJazz={playlistJazz}
            thumbnail={
              "https://cdn.mos.cms.futurecdn.net/oCtbBypcUdNkomXw7Ryrtf-650-80.jpg.webp"
            }
            onClick={() => handlePlaylistClick("Rap", setCurrentPlace)}
          />
        </div>
        <div class="Playlist4">
          <Playlist
            name="Hip-hop"
            playlistHiphop={playlistHiphop}
            thumbnail={
              "https://cdn.mos.cms.futurecdn.net/oCtbBypcUdNkomXw7Ryrtf-650-80.jpg.webp"
            }
            onClick={() => handlePlaylistClick("Jazz", setCurrentPlace)}
          />
        </div>
      </div>
      <h2 className="recommended-title">Recommended Playlists Based on Mood</h2>
      <div className="header-line" />
      <div class="container">
        <div class="Playlist1">
          <Playlist
            name="Happy"
            thumbnail={
              "https://cdn.mos.cms.futurecdn.net/oCtbBypcUdNkomXw7Ryrtf-650-80.jpg.webp"
            }
            onClick={() => handlePlaylistClick("Happy", setCurrentPlace)}
          />
        </div>
        <div class="Playlist2">
          <Playlist
            name="Rock"
            thumbnail={
              "https://cdn.mos.cms.futurecdn.net/oCtbBypcUdNkomXw7Ryrtf-650-80.jpg.webp"
            }
            onClick={() => handlePlaylistClick("Rock", setCurrentPlace)}
          />
        </div>
        <div class="Playlist3">
          <Playlist
            name="Chill"
            thumbnail={
              "https://cdn.mos.cms.futurecdn.net/oCtbBypcUdNkomXw7Ryrtf-650-80.jpg.webp"
            }
            onClick={() => handlePlaylistClick("Chill", setCurrentPlace)}
          />
        </div>
        <div class="Playlist4">
          <Playlist
            name="Jazz"
            thumbnail={
              "https://cdn.mos.cms.futurecdn.net/oCtbBypcUdNkomXw7Ryrtf-650-80.jpg.webp"
            }
            onClick={() => handlePlaylistClick("Jazz", setCurrentPlace)}
          />
        </div>
      </div>
    </div>
  );
};

export default MainMiddle;
