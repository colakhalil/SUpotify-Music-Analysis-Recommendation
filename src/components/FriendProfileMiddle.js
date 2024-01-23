import React, { useEffect, useState } from "react";
import axios from "axios";
import UserPart from "./subcomponents/UserPart";
import Playlist from "./subcomponents/Playlist";
import FavoriteSongs90s from "./subcomponents/FavoriteSongs90s";
import FavoriteRecentSongs from "./subcomponents/FavoriteRecentSongs";
import MonthlyAverageRatingsChart from "./subcomponents/MonthlyAverageRatingsChart";
import SongsAddedByPerformerChart from "./subcomponents/SongsAddedByPerformerChart";
import globalVar from "../global";
import html2canvas from "html2canvas";

const handleScreenshotDownload = () => {
  html2canvas(document.body).then((canvas) => {
    const image = canvas
      .toDataURL("image/png")
      .replace("image/png", "image/octet-stream");
    const link = document.createElement("a");
    link.download = "screenshot.png";
    link.href = image;
    link.click();
  });
};

const FriendProfileMiddle = ({ friendName }) => {
  const [friendData, setFriendData] = useState(null);
  const [lastPlaylists, setLastPlaylists] = useState([]);

  useEffect(() => {
    const fetchFriendData = async () => {
      try {
        // Assuming friendName is the user_id required by your API
        const response = await axios.get(
          "http://127.0.0.1:8008/user_data_username/" + friendName
        );
        setFriendData(response.data);
      } catch (error) {
        console.error("Error fetching friend data:", error);
      }
    };

    fetchFriendData();
  }, [friendName]);

  const handleRated = () => {
    console.log("Export all rated songs clicked");
    let username = globalVar.username;
    // Fetch the data from the API
    axios
      .get("http://127.0.0.1:8008/" + username + "/all_rated_songs")
      .then((response) => {
        // Convert the response data to a JSON string
        const jsonString = JSON.stringify(response.data);
        // Create a Blob with the JSON string
        const blob = new Blob([jsonString], { type: "application/json" });
        // Create a link element
        const link = document.createElement("a");
        // Set the download attribute with a filename
        link.download = "all_rated_songs.json";
        // Create a URL for the Blob and set it as the href
        link.href = window.URL.createObjectURL(blob);
        // Append the link to the body
        document.body.appendChild(link);
        // Programmatically click the link to trigger the download
        link.click();
        // Remove the link from the body
        document.body.removeChild(link);
      })
      .catch((error) => {
        console.error("Error exporting all rated songs:", error);
      });
  };

  const handleHighRated = () => {
    console.log("Export highly rated songs clicked");

    // Replace '<current_user_id>' with the actual current user ID variable
    const userId = globalVar.username; // You would replace this with the actual user ID
    const apiEndpoint = `http://127.0.0.1:8008/${userId}/most_rated_songs`;

    axios
      .get(apiEndpoint)
      .then((response) => {
        // Convert the response data to a JSON string
        const jsonString = JSON.stringify(response.data);
        // Create a Blob with the JSON string
        const blob = new Blob([jsonString], { type: "application/json" });
        // Create a link element
        const link = document.createElement("a");
        // Set the download attribute with a filename
        link.download = "most_rated_songs.json";
        // Create a URL for the Blob and set it as the href
        link.href = window.URL.createObjectURL(blob);
        // Append the link to the body
        document.body.appendChild(link);
        // Programmatically click the link to trigger the download
        link.click();
        // Remove the link from the body
        document.body.removeChild(link);
      })
      .catch((error) => {
        console.error("Error exporting highly rated songs:", error);
      });
  };

  return (
    <>
      <div className="main-container">
        <div className="content-container">
          <UserPart userData={friendData} /> ,
          {/* UserPart bileşenini burada kullan */}
          <FavoriteSongs90s userName={friendName} />
          <FavoriteRecentSongs userName={friendName} />
          <div className="charts-container" style={{ display: "flex" }}>
            <div className="chart-wrapper">
              <MonthlyAverageRatingsChart userName={friendName} />
            </div>
            <div className="chart-wrapper">
              <SongsAddedByPerformerChart userName={friendName} />
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default FriendProfileMiddle;
