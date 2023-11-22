import React from "react";
import { useParams, useLocation } from 'react-router-dom';
import FriendPart from "./subcomponents/FriendPart";
import FriendPlaylists from "./subcomponents/FriendPlaylists";
import FavoriteArtists from "./subcomponents/FavoriteArtists";
import FavoriteGenres from "./subcomponents/FavoriteGenres";
import FriendActivityChart from "./subcomponents/FriendActivityChart";
import TopSongsChart from "./subcomponents/TopSongsChart";


const FriendProfileMiddle = ({ friendPlaylists = [], friendData}) => {
  return(
    <p>merhaba!</p>

  );
  {/*
  const { friendName } = useParams(); // get the friend name from the URL parameter
  const location = useLocation();
  const locationFriendData = location.state?.friendData;

  // Use locationFriendData if available, otherwise use friendData from props
  const effectiveFriendData = locationFriendData || friendData;

  const handlePlaylistClick = (playlistName) => {
    setCurrentPlace("playlist");
    console.log(`Playlist clicked: ${playlistName}`);
    // Handle the playlist click event, such as navigating to the playlist page.
  };

  const handleArtistClick = (artistName) => {
    setCurrentPlace("artist");
    console.log(`Artist clicked: ${artistName}`);
    // Handle the artist click event, such as navigating to the artist's page.
  };
  console.log("Friend playlists:", friendPlaylists);

  return (
    <>
      <div className="main-container">
        <div className="content-container">
          <FriendPart friendData={effectiveFriendData} />
          <h2 className="friend-playlists-title">Friend's Playlists</h2>
          <div className="friendPlaylists-container-forPP">
          {Array.isArray(friendPlaylists) && friendPlaylists.map((playlist, index) => (
            <FriendPlaylists
                key={index}
                name={playlist.name}
                thumbnail={playlist.thumbnail}
                onClick={() => handlePlaylistClick(playlist.name)}
              />
            ))}
          </div>
          <FavoriteArtists onArtistClick={handleArtistClick} />
          <FavoriteGenres />
          <FriendActivityChart />
          <TopSongsChart />
        </div>
      </div>
    </>
  );
          */}
};

export default FriendProfileMiddle;
