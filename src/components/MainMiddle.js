import React from "react";
import SearchBar from "./subcomponents/SearchBar";
import Playlist from "./subcomponents/Playlist";
import { useState, useEffect } from "react";
import globalVar from "../global";
import axios from "axios";

const MainMiddle = ({
  setCurrentPlace,
  popPlaylist,
  rockPlaylist,
  jazzPlaylist,
  friendsUpdate,
  housePlaylist,
  happyPlaylist,
  sadPlaylist,
  studyPlaylist,
  chillPlaylist,
  setCurrentPlaylistInfo,
  setSearchedArray,
  friendsData,
}) => {
  const handlePlaylistClick = (playlistName, setCurrentPlace) => {
    setCurrentPlace("playlist");

    const playlists = {
      pop: { ...popPlaylist, name: "Pop" },
      rock: { ...rockPlaylist, name: "Rock" },
      jazz: { ...jazzPlaylist, name: "Jazz" },
      house: { ...housePlaylist, name: "House" },

      happy: { ...happyPlaylist, name: "Happy" },
      sad: { ...sadPlaylist, name: "Sad" },
      study: { ...studyPlaylist, name: "Study" },
      chill: { ...chillPlaylist, name: "Chill" },

      friendrecommendation: {
        ...friendPlaylist,
        name: "Friend Recommendation",
      },
    };

    setCurrentPlaylistInfo(playlists[playlistName.toLowerCase()]);
    // Here you would handle the click event, such as navigating to the playlist page.
  };

  const [friendPlaylist, setFriendPlaylist] = useState({
    url: "https://cdn.mos.cms.futurecdn.net/oCtbBypcUdNkomXw7Ryrtf-650-80.jpg.webp",
    songs: [],
  });
  function transformData(apiData) {
    // Assuming apiData is the object you receive from your API
    const transformedData = {
      songs: apiData.recommendations.map((song) => ({
        artistName: song.artist_name,
        id: song.song_id,
        songLength: song.songLength,
        songName: song.song_name,
      })),
      url:
        apiData.recommendations.length > 0
          ? apiData.recommendations[0].picture
          : "https://cdn.mos.cms.futurecdn.net/oCtbBypcUdNkomXw7Ryrtf-650-80.jpg.webp",
    };

    return transformedData;
  }

  useEffect(() => {
    setFriendPlaylist({
      url: "https://cdn.mos.cms.futurecdn.net/oCtbBypcUdNkomXw7Ryrtf-650-80.jpg.webp",
      songs: [],
    });
    const fetchData = async () => {
      try {
        const response = await axios.get(
          `http://127.0.0.1:8008/${globalVar.username}/friends_recommendations`
        );

        if (transformData.length != 0) {
          const formattedData = transformData(response.data);
          setFriendPlaylist(formattedData);
        }
      } catch (error) {
        console.error("Error fetching data: ", error);
        // Handle the error appropriately
      }
    };

    fetchData();
  }, [friendsUpdate]); // Dependency array, useEffect will run when globalVar.username changes
  useEffect(() => {
    // When friendsData changes, update the key to force re-render
    setPlaylistKey((prevKey) => prevKey + 1);
  }, [friendsData]);
  const [playlistKey, setPlaylistKey] = useState(0);
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
      <h2 className="recommended-title">Recommended Playlists Friends</h2>
      <div className="header-line" />
      <div class="container">
        <Playlist
          key={playlistKey}
          name={
            "Based On " +
            friendsData
              .map((friend) => {
                // If last listened song is private, only return the friend's name
                if (friend.lastListenedSong != "private") {
                  return friend.name;
                } else {
                  // If the last listened song is not private, you can include it
                  // Adjust this part according to your data structure and requirements
                  return "";
                }
              })
              .join(" ")
          }
          playlistData={friendPlaylist}
          thumbnail={
            friendPlaylist.url ||
            "https://cdn.mos.cms.futurecdn.net/oCtbBypcUdNkomXw7Ryrtf-650-80.jpg.webp"
          }
          onClick={() =>
            handlePlaylistClick("friendrecommendation", setCurrentPlace)
          }
        />
      </div>
    </div>
  );
};

export default MainMiddle;