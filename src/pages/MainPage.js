import React, { useState, useEffect } from "react";
import "../pagesCSS/MainPage.css";
import LeftBar from "../components/LeftBar";
import FriendActivity from "../components/FriendActivity";
import BottomBar from "../components/BottomBar";
import LyrcsMiddle from "../components/LyrcsMiddle";


import MainMiddle from "../components/MainMiddle";
import ProfileMiddle from "../components/ProfileMiddle";
import PlaylistMiddle from "../components/PlaylistMiddle";
import SubmissionForm from "../components/SubmissionForm";
import SubmissionFormExport from "../components/SubmissionFormExport";
import FriendProfileMiddle from "../components/FriendProfileMiddle";

const MainPage = () => {
  const [currentPlace, setCurrentPlace] = useState("main");
  const [currentPlaylistInfo, setCurrentPlaylistInfo] = useState(null);

  // DUMMY DATALAR
  const [popPlaylist, setPopPlaylist] = useState({ songs: [] });
  const [rockPlaylist, setRockPlaylist] = useState({ songs: [] });
  const [jazzPlaylist, setJazzPlaylist] = useState({ songs: [] });
  const [housePlaylist, setHousePlaylist] = useState({ songs: [] });

  const [happyPlaylist, setHappyPlaylist] = useState({ songs: [] });
  const [sadPlaylist, setSadPlaylist] = useState({ songs: [] });
  const [studyPlaylist, setStudyPlaylist] = useState({ songs: [] });
  const [chillPlaylist, setChillPlaylist] = useState({ songs: [] });



    
      const getSongsByGenre = async (genre) => {
        try {
          const response = await fetch(`http://127.0.0.1:8008/recommendations/${genre}`);
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          const data = await response.json();
          console.log('Fetched data:', data); // Check the structure of the fetched data
      
          const formattedSongs = data.tracks.map((track) => ({
            songName: track.name,
            artistName: track.artists.map((artist) => artist.name).join(", "),
            songLength: track.duration_ms,
            releaseYear: new Date(track.album.release_date).getFullYear(),
            rating: track.popularity,
            album: track.album.name,
            songPicture: track.album.images[0].url,
          }));
      
          return formattedSongs;
        } catch (error) {
          console.error("Error fetching data:", error);
          return [];
        }
      };
      
    
      

      useEffect(() => {
        getSongsByGenre('pop').then((songs) => setPopPlaylist({ songs }));
        getSongsByGenre('rock').then((songs) => setRockPlaylist({ songs }));
        getSongsByGenre('jazz').then((songs) => setJazzPlaylist({ songs }));
        getSongsByGenre('house').then((songs) => setHousePlaylist({ songs }));
        
        getSongsByGenre('happy').then((songs) => setHappyPlaylist({ songs }));
        getSongsByGenre('sad').then((songs) => setSadPlaylist({ songs }));
        getSongsByGenre('study').then((songs) => setStudyPlaylist({ songs }));
        getSongsByGenre('chill').then((songs) => setChillPlaylist({ songs }));
      }, []);
    


  // Rest of your component code

  const playlistData = {
    playlistID: "playlist123",
    playlistName: "Chill Vibes",
    playlistPicture:
      "https://cdn.mos.cms.futurecdn.net/oCtbBypcUdNkomXw7Ryrtf-650-80.jpg.webp",
    songs: [
      {
        songName: "Ocean Breeze",
        duration: "3:45",
        releaseYear: 2021,
        artist: "Tropical Sound",
        songRating: 4.5,
      },
      {
        songName: "Mountain Serenity",
        duration: "4:20",
        releaseYear: 2020,
        artist: "Nature Melody",
        songRating: 4.7,
      },
      {
        songName: "Urban Sunset",
        duration: "5:00",
        releaseYear: 2019,
        artist: "City Lights",
        songRating: 4.3,
      },
      {
        songName: "Virginia Beach",
        duration: "5:00",
        releaseYear: 2023,
        artist: "City Lights",
        songRating: 4.3,
      },
      // Add more songs as needed
    ],
  };

  const userData = {
    username: "UserName",
    profilePicture:
      "https://d1csarkz8obe9u.cloudfront.net/posterpreviews/artistic-album-cover-design-template-d12ef0296af80b58363dc0deef077ecc_screen.jpg?ts=1696331695", // Profil resminin yolunu güncelleyin
    friendCount: 5, // Arkadaş sayısını güncelleyin
  };

  // Son calınan 4 playlıst
  const lastPlaylists = [
    {
      name: "Playlist 1",
      thumbnail:
        "https://cdn.mos.cms.futurecdn.net/oCtbBypcUdNkomXw7Ryrtf-650-80.jpg.webp",
    },
    {
      name: "Playlist 2",
      thumbnail:
        "https://cdn.mos.cms.futurecdn.net/oCtbBypcUdNkomXw7Ryrtf-650-80.jpg.webp",
    },
    {
      name: "Playlist 3",
      thumbnail:
        "https://cdn.mos.cms.futurecdn.net/oCtbBypcUdNkomXw7Ryrtf-650-80.jpg.webp",
    },
    {
      name: "Playlist 3",
      thumbnail:
        "https://cdn.mos.cms.futurecdn.net/oCtbBypcUdNkomXw7Ryrtf-650-80.jpg.webp",
    },
    {
      name: "Playlist 3",
      thumbnail:
        "https://cdn.mos.cms.futurecdn.net/oCtbBypcUdNkomXw7Ryrtf-650-80.jpg.webp",
    },
    {
      name: "Playlist 3",
      thumbnail:
        "https://cdn.mos.cms.futurecdn.net/oCtbBypcUdNkomXw7Ryrtf-650-80.jpg.webp",
    },

    // Add more playlists as needed
  ];

  const song = {
    title: "Çingenem",
    artist: "Ebru Gündeş",
    duration: "2:48",
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
  // DUMMY DATALAR
  return (
    <>
      <div className="main-container">
        <LeftBar playlists={playlists} setCurrentPlace={setCurrentPlace} />

        {currentPlace === "main" && (
          <MainMiddle setCurrentPlace={setCurrentPlace}
          popPlaylist={popPlaylist}
          rockPlaylist={rockPlaylist}
          jazzPlaylist={jazzPlaylist}
          housePlaylist={housePlaylist}
          happyPlaylist= {happyPlaylist}
          sadPlaylist= {sadPlaylist}
          studyPlaylist= {studyPlaylist}
          chillPlaylist= {chillPlaylist}
          setCurrentPlaylistInfo={setCurrentPlaylistInfo}
          ></MainMiddle>
        )}
        {currentPlace === "submit-form" && <SubmissionForm></SubmissionForm>}
        {currentPlace === "submit-formE" && (
          <SubmissionFormExport></SubmissionFormExport>
        )}
          {currentPlace === "profile" && (
          <ProfileMiddle
            userData={userData}
            setCurrentPlace={setCurrentPlace}
          ></ProfileMiddle>
        )}

        {currentPlace === "playlist" && (
          <PlaylistMiddle
            playlistInfo={currentPlaylistInfo}
          />
        )}
        {currentPlace === "lyrc" && <LyrcsMiddle song={song}></LyrcsMiddle>}
   
        <FriendActivity
          friendsData={friendsData}
          setCurrentPlace={setCurrentPlace}
        />
        {currentPlace === "friend" && (
          <FriendProfileMiddle></FriendProfileMiddle>
        )}
        <BottomBar song={song} setCurrentPlace={setCurrentPlace} />
      </div>
    </>
  );
};
export default MainPage;
