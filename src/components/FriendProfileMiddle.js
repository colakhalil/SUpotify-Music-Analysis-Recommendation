import React, { useEffect, useState } from "react";
import axios from "axios";
// Correct import for a default export
import FriendUserPart from './subcomponents/FriendUserPart';
import FriendFavoriteSongs from "./subcomponents/FavoriteSongs90s";
import FriendRecentActivity from "./subcomponents/FavoriteRecentSongs";
import globalVar from "../global";
import "../pagesCSS/FriendProfile.css";


// Updated dummy friend data with friendName
const dummyFriendData = {
  friendName: "İdil Güler",
  profilePicture: "/path/to/friend/profile/picture.jpg", // replace with actual path
  numberOfFriends: 50,
};

const FriendProfileMiddle = ({ friendEmail, setCurrentPlace }) => {
  const [friendData, setFriendData] = useState(dummyFriendData); // Using dummy data
  const [lastPlaylists, setLastPlaylists] = useState([]);

  // Simulate fetching friend's data
  useEffect(() => {
    // Simulate API call with a timeout
    setTimeout(() => {
      console.log("Simulated fetch of friend data:", dummyFriendData);
      setFriendData(dummyFriendData);
    }, 1000);
  }, [friendEmail]);

  // Ensure you have a profile picture URL, either from data or a placeholder
  const profilePic = friendData.profilePicture || "path/to/default/profile.jpg";

  const handlePlaylistClick = (playlistName) => {
    setCurrentPlace("playlist");
    console.log(`Playlist clicked: ${playlistName}`);
  };

  return (
    <div className="main-container">
      <div className="content-container">
        <FriendUserPart friendData={friendData} />
        <FriendFavoriteSongs albumsData={friendData.favorite90sAlbums} />
        <FriendRecentActivity songsData={friendData.recentSongs} />
      </div>
    </div>
  );
  
};

export default FriendProfileMiddle;

