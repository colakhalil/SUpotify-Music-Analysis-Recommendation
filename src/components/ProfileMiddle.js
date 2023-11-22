import React, { useEffect, useState } from "react";
import axios from "axios";
import UserPart from "./subcomponents/UserPart";
import Playlist from "./subcomponents/Playlist";
import FavoriteSongs90s from "./subcomponents/FavoriteSongs90s";
import FavoriteRecentSongs from "./subcomponents/FavoriteRecentSongs";
import MonthlyAverageRatingsChart from "./subcomponents/MonthlyAverageRatingsChart";
import SongsAddedByPerformerChart from "./subcomponents/SongsAddedByPerformerChart";
import globalVar from "../global";

const ProfileMiddle = ({ setCurrentPlace }) => {
  const [userData, setUserData] = useState(null);
  const [lastPlaylists, setLastPlaylists] = useState([]);

  useEffect(() => {
    // Use your specific API endpoint

    const apiEndpoint = "http://127.0.0.1:8008/user_data/" + globalVar.mail;
    console.log("globalmail " + globalVar.mail);

    axios
      .get(apiEndpoint)
      .then((response) => {
        setUserData(response.data);

        // Assuming response.data contains lastPlaylists
        setLastPlaylists(response.data.lastPlaylists);

        // Print the fetched data to the console
        console.log("Fetched user data:", response.data);
      })
      .catch((error) => {
        console.error("API request error:", error);
      });
  }, []);

  const handlePlaylistClick = (playlistName) => {
    setCurrentPlace("playlist");
    console.log(`Playlist clicked: ${playlistName}`);
  };

  const handleButtonClick = () => {
    setCurrentPlace("submit-form");
    console.log("Button clicked");
  };

  const handleButtonClickE = () => {
    setCurrentPlace("submit-formE");
    console.log("Button clicked");
  };

  return (
    <>
      <div className="main-container">
        <div className="content-container">
          <UserPart userData={userData} />{" "}
          <button onClick={handleButtonClick} className="add-song-btn">
            Add song to the database
          </button>
          {/* UserPart bileşenini burada kullan */}
          <h2 className="recommended-title">Your Playlists </h2>
          <div className="lastPlaylists-container-forPP">
            <Playlist
              name="Jazz"
              thumbnail={
                "https://cdn.mos.cms.futurecdn.net/oCtbBypcUdNkomXw7Ryrtf-650-80.jpg.webp"
              }
              onClick={() => handlePlaylistClick("Jazz", setCurrentPlace)}
            />
          </div>
          <FavoriteSongs90s />
          <FavoriteRecentSongs />
          <MonthlyAverageRatingsChart />
          <SongsAddedByPerformerChart />
        </div>
      </div>
    </>
  );
};

export default ProfileMiddle;
