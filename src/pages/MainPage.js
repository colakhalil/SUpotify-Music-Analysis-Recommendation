import React, { useState, useEffect } from "react";
import "../pagesCSS/MainPage.css";
import LeftBar from "../components/LeftBar";
import FriendActivity from "../components/FriendActivity";
import BottomBar from "../components/BottomBar";
import SearchBar from "../components/subcomponents/SearchBar";
import Playlist from "../components/subcomponents/Playlist";



const MainPage = () => {


  // Dummy verileri temsil eden bir JSON objesi
const userData = {
  username: 'UserName',
  profilePicture: "https://d1csarkz8obe9u.cloudfront.net/posterpreviews/artistic-album-cover-design-template-d12ef0296af80b58363dc0deef077ecc_screen.jpg?ts=1696331695", // Profil resminin yolunu güncelleyin
  friendCount: 5 // Arkadaş sayısını güncelleyin
};







    // Son calınan 4 playlıst
  const lastPlaylists = [
    { name: 'Playlist 1', thumbnail: 'https://cdn.mos.cms.futurecdn.net/oCtbBypcUdNkomXw7Ryrtf-650-80.jpg.webp' },
    { name: 'Playlist 2', thumbnail: 'https://cdn.mos.cms.futurecdn.net/oCtbBypcUdNkomXw7Ryrtf-650-80.jpg.webp' },
    { name: 'Playlist 3', thumbnail: 'https://cdn.mos.cms.futurecdn.net/oCtbBypcUdNkomXw7Ryrtf-650-80.jpg.webp' },
    { name: 'Playlist 3', thumbnail: 'https://cdn.mos.cms.futurecdn.net/oCtbBypcUdNkomXw7Ryrtf-650-80.jpg.webp' },
    { name: 'Playlist 3', thumbnail: 'https://cdn.mos.cms.futurecdn.net/oCtbBypcUdNkomXw7Ryrtf-650-80.jpg.webp' },
    { name: 'Playlist 3', thumbnail: 'https://cdn.mos.cms.futurecdn.net/oCtbBypcUdNkomXw7Ryrtf-650-80.jpg.webp' },

    // Add more playlists as needed
  ];
  const recomendedPlaylists= [
    { name: 'Mix 1', thumbnail: 'https://cdn.mos.cms.futurecdn.net/oCtbBypcUdNkomXw7Ryrtf-650-80.jpg.webp' },
    { name: 'Mix 2', thumbnail: 'https://cdn.mos.cms.futurecdn.net/oCtbBypcUdNkomXw7Ryrtf-650-80.jpg.webp' },
    { name: 'Mix 3', thumbnail: 'https://cdn.mos.cms.futurecdn.net/oCtbBypcUdNkomXw7Ryrtf-650-80.jpg.webp' },
    { name: 'Mix 4', thumbnail: 'https://cdn.mos.cms.futurecdn.net/oCtbBypcUdNkomXw7Ryrtf-650-80.jpg.webp' },
    { name: 'Mix 5', thumbnail: 'https://cdn.mos.cms.futurecdn.net/oCtbBypcUdNkomXw7Ryrtf-650-80.jpg.webp' },
    { name: 'Mix 6', thumbnail: 'https://cdn.mos.cms.futurecdn.net/oCtbBypcUdNkomXw7Ryrtf-650-80.jpg.webp' },
    { name: 'Mix 7', thumbnail: 'https://cdn.mos.cms.futurecdn.net/oCtbBypcUdNkomXw7Ryrtf-650-80.jpg.webp' },
    { name: 'Mix 8', thumbnail: 'https://cdn.mos.cms.futurecdn.net/oCtbBypcUdNkomXw7Ryrtf-650-80.jpg.webp' },

  ]

  const song = {
    title: "Beni Böyle Hatırla",
    artist: "Çetin Dilşiz",
    duration: "2:48",
    lyrics: "Here would be the lyrics of the song...",
    genre: "Pop, Dance",
    mood: "Uplifting",
    recordingType: "Studio",
    instruments: "Guitar, Piano, Drums",
    playCount: 100,
    releaseYear: 2021,
    dateAdded: "2023-04-15",
    userPrevRating: 2,
    img: "https://d1csarkz8obe9u.cloudfront.net/posterpreviews/artistic-album-cover-design-template-d12ef0296af80b58363dc0deef077ecc_screen.jpg?ts=1696331695",
  };

  const friendsData = [
    {
      name: "Idil Güler",
      lastListenedSong: "Song Name 1",
      profilePicture:
        "https://d1csarkz8obe9u.cloudfront.net/posterpreviews/artistic-album-cover-design-template-d12ef0296af80b58363dc0deef077ecc_screen.jpg?ts=1696331695",
    },
    {
      name: "Umit Colak",
      lastListenedSong: "Song Name 2",
      profilePicture:
        "https://d1csarkz8obe9u.cloudfront.net/posterpreviews/artistic-album-cover-design-template-d12ef0296af80b58363dc0deef077ecc_screen.jpg?ts=1696331695",
    },
    {
      name: "Halil Colak",
      lastListenedSong: "Song Name 3",
      profilePicture:
        "https://d1csarkz8obe9u.cloudfront.net/posterpreviews/artistic-album-cover-design-template-d12ef0296af80b58363dc0deef077ecc_screen.jpg?ts=1696331695",
    },
    // Add more friend objects
  ];
  // Dummy data for playlists
  const playlists = [
    {
      playlist_name: "EFKARLI IKEN",
      playlist_picture:
        "https://d1csarkz8obe9u.cloudfront.net/posterpreviews/artistic-album-cover-design-template-d12ef0296af80b58363dc0deef077ecc_screen.jpg?ts=1696331695",
      song_number: "12949129412",
    },
    {
      playlist_name: "GAZLAAAAAAA",
      playlist_picture:
        "https://d1csarkz8obe9u.cloudfront.net/posterpreviews/artistic-album-cover-design-template-d12ef0296af80b58363dc0deef077ecc_screen.jpg?ts=1696331695",
      song_number: "124124",
    },
    {
      playlist_name: "HANIMI DUSUNURKEN",
      playlist_picture:
        "https://d1csarkz8obe9u.cloudfront.net/posterpreviews/artistic-album-cover-design-template-d12ef0296af80b58363dc0deef077ecc_screen.jpg?ts=1696331695",
      song_number: "9999999999",
    },
    // Add more playlists here...
  ];

  const handleSearch = (searchTerm) => {
    console.log(`Search term submitted: ${searchTerm}`);
    // You can now do something with the search term, 
    // like making an API call to fetch search results
  };
  const handlePlaylistClick = (playlistName) => {
    console.log(`Playlist clicked: ${playlistName}`);
    // Here you would handle the click event, such as navigating to the playlist page.
  };
  // when song is updated this BottomBar also will be updated automatically
  return (
    <>  
      <div className="main-container">
        <LeftBar playlists={playlists}/>
          <div className="content-container">
            <SearchBar onSearch={handleSearch}/>
            <h2 className="last-played-title">Your last played Playlists </h2>
            <div className="lastPlaylists-container">
              {lastPlaylists.map((lastPlaylists, index) => (
                <Playlist
                  key={index}
                  name={lastPlaylists.name}
                  thumbnail={lastPlaylists.thumbnail}
                  onClick={() => handlePlaylistClick(lastPlaylists.name)}
            
                />
              ))}
            </div>
             <h2 className="recommended-playlists">Recomended Playlists</h2>
             <div className="recomended-playlists-container">
              {recomendedPlaylists.map((recomendedPlaylists, index) => (
                <Playlist
                  key={index}
                  name={recomendedPlaylists.name}
                  thumbnail={recomendedPlaylists.thumbnail}
                  onClick={() => handlePlaylistClick(recomendedPlaylists.name)}
            
                />
              ))}
            </div>
          </div>
          
        <FriendActivity friendsData={friendsData} />
        <BottomBar song={song} />
      </div>
    </>

  );
};
export default MainPage;
