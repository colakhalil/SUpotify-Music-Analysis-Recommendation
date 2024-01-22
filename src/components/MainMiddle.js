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

  const enrichablePlaylists = new Set(["Pop", "Rock", "Jazz", "House", "Happy", "Sad", "Study", "Chill"]);


  
  const handlePlaylistClick = (playlistName, setCurrentPlace) => {
    
    setCurrentPlace("playlist");

    const enrichAllowedPlaylists = ["Pop", "Rock", "Jazz", "House", "Happy", "Sad", "Study", "Chill"];

    // Build the enriched playlist object only for allowed playlists
    const buildEnrichedPlaylist = (basePlaylist, name) => {
      return {
        ...basePlaylist,
        name,
        isEnrichAllowed: enrichAllowedPlaylists.includes(name),
      };
    };

    const playlists = {
      pop: buildEnrichedPlaylist(popPlaylist, "Pop"),
      rock: buildEnrichedPlaylist(rockPlaylist, "Rock"),
      jazz: buildEnrichedPlaylist(jazzPlaylist, "Jazz"),
      house: buildEnrichedPlaylist(housePlaylist, "House"),
      happy: buildEnrichedPlaylist(happyPlaylist, "Happy"),
      sad: buildEnrichedPlaylist(sadPlaylist, "Sad"),
      study: buildEnrichedPlaylist(studyPlaylist, "Study"),
      chill: buildEnrichedPlaylist(chillPlaylist, "Chill"),
      // Other playlists should have isEnrichAllowed set to false by default
      friendrecommendation: { ...friendPlaylist, name: "Friend Recommendation" },
      recommendedartistsongs: { ...recommendedArtistSongs, name: "Recommended Artist Songs" },
      newlyratedrecommendation: { ...newlyRatedRecommendation, name: "Based on Newly Rated Songs" },
      geolocationrecommendaiton: { ...geolocationRecommendation, name: "Based on Your Geolocation" },
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
  const [selectedCity, setSelectedCity] = useState("");
  const [concerts, setConcerts] = useState([]);

  const handleCitySelect = async (e) => {
    setSelectedCity(e.target.value);
    const city = e.target.value;
    const url = `http://127.0.0.1:8008/concerts/${city.toLowerCase()}`;

    try {
      const response = await fetch(url);
      const data = await response.json();
      setConcerts(data);
    } catch (error) {
      console.error("Error fetching concerts:", error);
      // Handle error appropriately
    }
  };
  const countryCityMap = {
    Global: [
      "New York",
      "London",
      "Paris",
      "Tokyo",
      "Berlin",
      "Sydney",
      "Toronto",
      "Moscow",
      "Dubai",
      "Singapore",
    ],
    USA: [
      "New York",
      "Los Angeles",
      "Chicago",
      "Houston",
      "Phoenix",
      "Philadelphia",
      "San Antonio",
      "San Diego",
      "Dallas",
      "San Jose",
    ],
    Turkey: [
      "Istanbul",
      "Ankara",
      "Izmir",
      "Antalya",
      "Adana",
      "Bursa",
      "Gaziantep",
      "Konya",
      "Mersin",
      "Kayseri",
    ],
    Italy: [
      "Rome",
      "Milan",
      "Naples",
      "Turin",
      "Palermo",
      "Genoa",
      "Bologna",
      "Florence",
      "Bari",
      "Catania",
    ],
    France: [
      "Paris",
      "Marseille",
      "Lyon",
      "Toulouse",
      "Nice",
      "Nantes",
      "Strasbourg",
      "Montpellier",
      "Bordeaux",
      "Lille",
    ],
    Spain: [
      "Madrid",
      "Barcelona",
      "Valencia",
      "Seville",
      "Zaragoza",
      "Malaga",
      "Murcia",
      "Palma",
      "Las Palmas",
      "Bilbao",
    ],
    United_Kingdom: [
      "London",
      "Birmingham",
      "Manchester",
      "Glasgow",
      "Newcastle",
      "Sheffield",
      "Liverpool",
      "Leeds",
      "Bristol",
      "Belfast",
    ],
    Mexico: [
      "Mexico City",
      "Guadalajara",
      "Monterrey",
      "Puebla",
      "Tijuana",
      "Cancún",
      "Acapulco",
      "Mazatlán",
      "Chihuahua",
      "Oaxaca",
    ],
    Bolivia: [
      "Santa Cruz",
      "La Paz",
      "Cochabamba",
      "Oruro",
      "Sucre",
      "Tarija",
      "Potosí",
      "Trinidad",
      "Cobija",
      "Montero",
    ],
    Colombia: [
      "Bogotá",
      "Medellín",
      "Cali",
      "Barranquilla",
      "Cartagena",
      "Cúcuta",
      "Bucaramanga",
      "Pereira",
      "Santa Marta",
      "Ibagué",
    ],
    Bulgaria: [
      "Sofia",
      "Plovdiv",
      "Varna",
      "Burgas",
      "Ruse",
      "Stara Zagora",
      "Pleven",
      "Sliven",
      "Dobrich",
      "Shumen",
    ],
    Morocco: [
      "Casablanca",
      "Fez",
      "Tangier",
      "Marrakesh",
      "Rabat",
      "Meknes",
      "Oujda",
      "Kenitra",
      "Agadir",
      "Tetouan",
    ],
    South_Korea: [
      "Seoul",
      "Busan",
      "Incheon",
      "Daegu",
      "Daejeon",
      "Gwangju",
      "Suwon",
      "Ulsan",
      "Goyang",
      "Seongnam",
    ],
  };

  const [cities, setCities] = useState(countryCityMap["Global"]); // Default to global cities

  useEffect(() => {
    // Update cities when selectedCountry changes
    const availableCities = countryCityMap[selectedCountry] || [];
    setCities(availableCities);
    setSelectedCity(""); // Reset selected city when country changes
  }, [selectedCountry]);

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
          <label htmlFor="country-select">Select a Country:</label>
          <select
            id="country-select"
            onChange={handleCountrySelect}
            value={selectedCountry}
          >
            {Object.keys(countryCityMap).map((country) => (
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
      <div>
        <label htmlFor="city-select">Select a City:</label>
        <select
          id="city-select"
          onChange={handleCitySelect}
          value={selectedCity}
        >
          <option value="">Select City</option>
          {cities.map((city) => (
            <option key={city} value={city}>
              {city}
            </option>
          ))}
        </select>
      </div>

      {/* Display upcoming concerts */}
      <div className="artist-recommendations-container">
        {/* ... other artist recommendations ... */}
      </div>

      <div className="concerts-container">
        <h2>Upcoming Concerts in {selectedCity}</h2>
        <div className="concerts-list">
          {concerts.map((concert, index) => (
            <div className="concert-card" key={index}>
              <div className="concert-info">
                <p className="concert-date">Date: {concert.date}</p>
                <p className="concert-name">Name: {concert.name}</p>
                <p className="concert-venue">Venue: {concert.venue}</p>
              </div>
              <a
                className="concert-link"
                href={concert.url}
                target="_blank"
                rel="noopener noreferrer"
              >
                Buy Tickets
              </a>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default MainMiddle;
