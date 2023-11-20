import React from "react";
import UserPart from "./subcomponents/UserPart";
import Playlist from "./subcomponents/Playlist";

const ProfileMiddle = ({ lastPlaylists, userData, setCurrentPlace }) => {
  const handlePlaylistClick = (playlistName) => {
    setCurrentPlace("playlist");
    console.log(`Playlist clicked: ${playlistName}`);
    // Here you would handle the click event, such as navigating to the playlist page.
  };
  const handleButtonClick = () => {
    setCurrentPlace("submit-form");
    console.log("Button clicked");
  }
  return (
    <>
      <div className="main-container">
        <div className="content-container">
          <UserPart userData={userData} />{" "}
          <button 
          onClick={handleButtonClick}
          className="add-song-btn">Add song to the database</button>
          {/* UserPart bileşenini burada kullan */}
          <h2 className="last-played-title">Your Playlists </h2>
          
          <div className="lastPlaylists-container-forPP">
            {lastPlaylists.map((lastPlaylists, index) => (
              <Playlist
                key={index}
                name={lastPlaylists.name}
                thumbnail={lastPlaylists.thumbnail}
                onClick={() => handlePlaylistClick(lastPlaylists.name)}
              />
            ))}
          </div>
          {/* Diğer içerikler */}
        </div>
      </div>
    </>
  );
};

export default ProfileMiddle;
