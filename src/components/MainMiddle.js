import React from "react";
import SearchBar from "./subcomponents/SearchBar";
import Playlist from "./subcomponents/Playlist";
import { useState, useEffect } from "react";
import globalVar from "../global";
import axios from "axios";
import JoyRide from "react-joyride";
import RecommendArtist from "./subcomponents/RecommendArtist";

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
      recommendedartistsongs: {
        ...recommendedArtistSongs,
        name: "Recommended Artist Songs",
      },

      newlyratedrecommendation: {
        ...newlyRatedRecommendation,
        name: "Based on Newly Rated Songs",
      },
      geolocationrecommendaiton: {
        ...geolocationRecommendation,
        name: "Based on Your Geolocation",
      },
    };

    setCurrentPlaylistInfo(playlists[playlistName.toLowerCase()]);
    // Here you would handle the click event, such as navigating to the playlist page.
  };

  const [formattedSongs, setFormattedSongs] = useState([]);

  const [selectedCountry, setSelectedCountry] = useState("Global"); // Default selection

  const countries = [
    "Global",
    "USA",
    "Turkey",
    "Italy",
    "France",
    "Spain",
    "United Kingdom",
    "Mexico",
    "Bolivia",
    "Colombia",
    "Bulgaria",
    "Morocco",
    "South Korea",
  ];

  const handleCountrySelect = (e) => {
    setSelectedCountry(e.target.value);
  };

  useEffect(() => {
    // Define the URL
    const url = `http://127.0.0.1:8008/get_top_songs/${selectedCountry}`;
    // Send a GET request using the fetch API
    fetch(url)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json(); // Parse the response as JSON
      })
      .then((data) => {
        if (data.length !== 0) {
          const transformedData = {
            songs: data.map((item) => ({
              artistName: item.artist_name.join(", "), // Assuming artist_name is an array
              id: item.song_id,
              songLength: item.songLength,
              songName: item.song_name,
            })),
            url:
              data.length > 0
                ? data[0].picture
                : "https://cdn.mos.cms.futurecdn.net/oCtbBypcUdNkomXw7Ryrtf-650-80.jpg.webp",
          };
          console.log("Response data as JSON:", transformedData);
          setGeolocationRecommendation(transformedData);
        }
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  }, [selectedCountry]);
  const sendRecommendations = async () => {
    try {
      // Replace with your actual API URL and endpoint
      const response = await axios.get(
        `http://localhost:5000/send_recommendations/${globalVar.username}`
      );

      if (response.data.message) {
        alert("Recommendations sent successfully!");
      } else {
        alert("Failed to send recommendations.");
      }
    } catch (error) {
      console.error("Error sending recommendations:", error);
      alert("An error occurred while sending recommendations.");
    }
  };

  const [recommendedArtistSongs, setRecommendedArtistSongs] = useState({
    url: "https://cdn.mos.cms.futurecdn.net/oCtbBypcUdNkomXw7Ryrtf-650-80.jpg.webp",
    songs: [],
  });

  const [newlyRatedRecommendation, setNewlyRatedRecommendation] = useState({
    url: "https://cdn.mos.cms.futurecdn.net/oCtbBypcUdNkomXw7Ryrtf-650-80.jpg.webp",
    songs: [],
  });

  const [geolocationRecommendation, setGeolocationRecommendation] = useState({
    url: "https://cdn.mos.cms.futurecdn.net/oCtbBypcUdNkomXw7Ryrtf-650-80.jpg.webp",
    songs: [],
  });
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
    // Define the URL
    const url =
      "http://127.0.0.1:8008/" +
      globalVar.username +
      "/newly_rating_recomendations";

    // Send a GET request using the fetch API
    fetch(url)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json(); // Parse the response as JSON
      })
      .then((data) => {
        if (data.length !== 0) {
          const transformedData = {
            songs: data.map((item) => ({
              artistName: item.artist_name.join(", "), // Assuming artist_name is an array
              id: item.song_id,
              songLength: item.songLength,
              songName: item.song_name,
            })),
            url:
              data.length > 0
                ? data[0].picture
                : "https://cdn.mos.cms.futurecdn.net/oCtbBypcUdNkomXw7Ryrtf-650-80.jpg.webp",
          };
          console.log("Response data as JSON:", transformedData);
          setNewlyRatedRecommendation(transformedData);
        }
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  }, []);

  useEffect(() => {
    // Define the URL
    const url =
      "http://127.0.0.1:8008/" +
      globalVar.username +
      "/recommended_artist_songs";

    // Send a GET request using the fetch API
    fetch(url)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json(); // Parse the response as JSON
      })
      .then((data) => {
        if (data.length != 0) {
          const transformedData = {
            songs: data.song_recommendations.map((song) => ({
              artistName: song.artist_name,
              id: song.song_id,
              songLength: song.songLength,
              songName: song.song_name,
            })),
            url:
              data.song_recommendations.length > 0
                ? data.song_recommendations[0].picture
                : "https://cdn.mos.cms.futurecdn.net/oCtbBypcUdNkomXw7Ryrtf-650-80.jpg.webp",
          };
          console.log("Response data as JSON:", transformedData);
          setRecommendedArtistSongs(transformedData);
        }
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  }, []);

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
      <div className="search-and-recommend">
        <SearchBar
          setCurrentPlace={setCurrentPlace}
          setSearchedArray={setSearchedArray}
        />
        <button onClick={sendRecommendations}>
          Send Me Song Recommendations
        </button>
      </div>
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
      <h2 className="recommended-title">Some Other Recommendations</h2>
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
        <Playlist
          name="Recommended Artist Songs"
          playlistData={recommendedArtistSongs}
          thumbnail={
            recommendedArtistSongs.url ||
            "https://cdn.mos.cms.futurecdn.net/oCtbBypcUdNkomXw7Ryrtf-650-80.jpg.webp"
          }
          onClick={() =>
            handlePlaylistClick("recommendedartistsongs", setCurrentPlace)
          }
        />
        <Playlist
          name="Based on Newly Rated Songs"
          playlistData={newlyRatedRecommendation}
          thumbnail={
            newlyRatedRecommendation.url ||
            "https://cdn.mos.cms.futurecdn.net/oCtbBypcUdNkomXw7Ryrtf-650-80.jpg.webp"
          }
          onClick={() =>
            handlePlaylistClick("newlyratedrecommendation", setCurrentPlace)
          }
        />

        <div>
          <label style={{ color: "white" }} htmlFor="country-select">
            Select a Country:
          </label>
          <select
            id="country-select"
            onChange={handleCountrySelect}
            value={selectedCountry}
          >
            {countries.map((country) => (
              <option key={country} value={country}>
                {country}
              </option>
            ))}
          </select>
          <Playlist
            name="Based on GeoLocation"
            playlistData={geolocationRecommendation}
            thumbnail={
              geolocationRecommendation.url ||
              "https://cdn.mos.cms.futurecdn.net/oCtbBypcUdNkomXw7Ryrtf-650-80.jpg.webp"
            }
            onClick={() =>
              handlePlaylistClick("geolocationrecommendaiton", setCurrentPlace)
            }
          />
        </div>
      </div>
      <h2 className="recommended-title">Artist Recommendation</h2>
      <RecommendArtist currentUserId={globalVar.username} />
    </div>
  );
};

export default MainMiddle;
