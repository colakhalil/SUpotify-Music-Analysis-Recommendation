import React from "react";
import SearchBar from "./subcomponents/SearchBar";
import Playlist from "./subcomponents/Playlist";

const MainMiddle = ({
  setCurrentPlace,
  popPlaylist,
  rockPlaylist,
  jazzPlaylist,
  housePlaylist,
  happyPlaylist,
  sadPlaylist,
  studyPlaylist,
  chillPlaylist,
  setCurrentPlaylistInfo,
  setSearchedArray,
}) => {
  const handlePlaylistClick = (playlistName, setCurrentPlace) => {
    setCurrentPlace("playlist");
    console.log(`Playlist clicked: ${playlistName}`);

    const playlists = {
      pop: { ...popPlaylist, name: "Pop" },
      rock: { ...rockPlaylist, name: "Rock" },
      jazz: { ...jazzPlaylist, name: "Jazz" },
      house: { ...housePlaylist, name: "House" },

      happy: { ...happyPlaylist, name: "Happy" },
      sad: { ...sadPlaylist, name: "Sad" },
      study: { ...studyPlaylist, name: "Study" },
      chill: { ...chillPlaylist, name: "Chill" },
    };

    setCurrentPlaylistInfo(playlists[playlistName.toLowerCase()]);
    // Here you would handle the click event, such as navigating to the playlist page.
  };

  // when song is updated this BottomBar also will be updated automatically

  return (
    <div className="content-container">
      <SearchBar
        setCurrentPlace={setCurrentPlace}
        setSearchedArray={setSearchedArray}
      />
      <h2 className="recommended-title">
        Recommended Playlists Based on Genre
      </h2>
      <div className="header-line" />
      <div class="container">
        <div class="Playlist1">
          <Playlist
            name="Pop"
            playlistData={popPlaylist}
            thumbnail={
              popPlaylist.url ||
              "https://cdn.mos.cms.futurecdn.net/oCtbBypcUdNkomXw7Ryrtf-650-80.jpg.webp"
            }
            onClick={() => handlePlaylistClick("Pop", setCurrentPlace)}
          />
        </div>
        <div class="Playlist2">
          <Playlist
            name="Rock"
            playlistData={rockPlaylist}
            thumbnail={
              rockPlaylist.url ||
              "https://cdn.mos.cms.futurecdn.net/oCtbBypcUdNkomXw7Ryrtf-650-80.jpg.webp"
            }
            onClick={() => handlePlaylistClick("Rock", setCurrentPlace)}
          />
        </div>
        <div class="Playlist3">
          <Playlist
            name="Jazz"
            playlistData={jazzPlaylist}
            thumbnail={
              jazzPlaylist.url ||
              "https://cdn.mos.cms.futurecdn.net/oCtbBypcUdNkomXw7Ryrtf-650-80.jpg.webp"
            }
            onClick={() => handlePlaylistClick("Jazz", setCurrentPlace)}
          />
        </div>
        <div class="Playlist4">
          <Playlist
            name="House"
            playlistData={housePlaylist}
            thumbnail={
              housePlaylist.url ||
              "https://cdn.mos.cms.futurecdn.net/oCtbBypcUdNkomXw7Ryrtf-650-80.jpg.webp"
            }
            onClick={() => handlePlaylistClick("House", setCurrentPlace)}
          />
        </div>
      </div>
      <h2 className="recommended-title">Recommended Playlists Based on Mood</h2>
      <div className="header-line" />
      <div class="container">
        <div class="Playlist1">
          <Playlist
            name="Happy"
            playlistData={happyPlaylist}
            thumbnail={
              happyPlaylist.url ||
              "https://cdn.mos.cms.futurecdn.net/oCtbBypcUdNkomXw7Ryrtf-650-80.jpg.webp"
            }
            onClick={() => handlePlaylistClick("Happy", setCurrentPlace)}
          />
        </div>

        <div class="Playlist2">
          <Playlist
            name="Sad"
            playlistData={sadPlaylist}
            thumbnail={
              sadPlaylist.url ||
              "https://cdn.mos.cms.futurecdn.net/oCtbBypcUdNkomXw7Ryrtf-650-80.jpg.webp"
            }
            onClick={() => handlePlaylistClick("Sad", setCurrentPlace)}
          />
        </div>

        <div class="Playlist3">
          <Playlist
            name="Study"
            playlistData={studyPlaylist}
            thumbnail={
              studyPlaylist.url ||
              "https://cdn.mos.cms.futurecdn.net/oCtbBypcUdNkomXw7Ryrtf-650-80.jpg.webp"
            }
            onClick={() => handlePlaylistClick("Study", setCurrentPlace)}
          />
        </div>

        <div class="Playlist4">
          <Playlist
            name="Chill"
            playlistData={chillPlaylist}
            thumbnail={
              chillPlaylist.url ||
              "https://cdn.mos.cms.futurecdn.net/oCtbBypcUdNkomXw7Ryrtf-650-80.jpg.webp"
            }
            onClick={() => handlePlaylistClick("Chill", setCurrentPlace)}
          />
        </div>
      </div>
    </div>
  );
};

export default MainMiddle;
