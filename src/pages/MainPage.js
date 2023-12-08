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
import DatabaseMiddle from "../components/DatabaseMiddle";

const MainPage = () => {
  const [currentPlace, setCurrentPlace] = useState("main");
  const [currentPlaylistInfo, setCurrentPlaylistInfo] = useState(null);
  const [currentBottomSong, setCurrentBottomSong] = useState({
    id: "song_id",
    artists: "Ebru Gündeş",
    title: "Çingenem",
    thumbnail:
      "https://d1csarkz8obe9u.cloudfront.net/posterpreviews/artistic-album-cover-design-template-d12ef0296af80b58363dc0deef077ecc_screen.jpg?ts=1696331695",
    playCount: 100,
    popularity: 0.5,
    valence: 0.5,
    duration: "2:48",
    genre: "Pop, Dance",
    releaseYear: 2021,
    dateAdded: "2023-04-15",
    userPrevRating: 2,
  }); // Initialize with an empty object or initial song data

  // ... [other functions and states]

  const formatDuration = (durationMs) => {
    const minutes = Math.floor(durationMs / 60000);
    const seconds = ((durationMs % 60000) / 1000).toFixed(0);
    return `${minutes}:${seconds < 10 ? "0" : ""}${seconds}`;
  };
  const setCurrentBottomSongState = (song) => {
    const bottomSong = {
      title: song.songName,
      artist: song.artistName,
      duration: formatDuration(song.songLength),
      genre: 0, //The playlist name of the clicked song. If the song is in the Pop playlist. Genre should be Pop
      UserPrevRating: 0, // Default as zero.
      releaseYear: song.releaseYear,
      img: song.img,
    };
    // Set the state
    setCurrentBottomSong(bottomSong);
  };

  // DUMMY DATALAR
  const [popPlaylist, setPopPlaylist] = useState({
    songs: [],
    url: "",
  });
  const [rockPlaylist, setRockPlaylist] = useState({ songs: [], url: "" });
  const [jazzPlaylist, setJazzPlaylist] = useState({ songs: [], url: "" });
  const [housePlaylist, setHousePlaylist] = useState({ songs: [], url: "" });

  const [happyPlaylist, setHappyPlaylist] = useState({ songs: [], url: "" });
  const [sadPlaylist, setSadPlaylist] = useState({ songs: [], url: "" });
  const [studyPlaylist, setStudyPlaylist] = useState({ songs: [], url: "" });
  const [chillPlaylist, setChillPlaylist] = useState({ songs: [], url: "" });

  const getSongsByGenre = async (genre) => {
    try {
      const response = await fetch(
        `http://127.0.0.1:8008/recommendations/${genre}`
      );
      if (!response.ok) {
        throw new Error(
          `HTTP error! status:SIKINTI YOK LINK YANLIS ${response.status}`
        );
      }
      const data = await response.json();
      console.log("Fetched data:", data); // Check the structure of the fetched data

      const formattedSongs = data.map((track) => ({
        songName: track.song_name,
        artistName: track.artist_name,
        songLength: track.songLength,
        id: track.song_id,
        url: track.picture,
      }));

      return formattedSongs;
    } catch (error) {
      console.error("Error fetching data:", error);
      return [];
    }
  };
  const playlistUrl = (genre) => {
    switch (genre) {
      case "pop":
        setPopPlaylist((prev) => ({ ...prev, url: prev.songs[0]?.url }));
        break;
      case "rock":
        setRockPlaylist((prev) => ({ ...prev, url: prev.songs[0]?.url }));
        break;
      case "jazz":
        setJazzPlaylist((prev) => ({ ...prev, url: prev.songs[0]?.url }));
        break;
      case "house":
        setHousePlaylist((prev) => ({ ...prev, url: prev.songs[0]?.url }));
        break;
      case "happy":
        setHappyPlaylist((prev) => ({ ...prev, url: prev.songs[0]?.url }));
        break;
      case "sad":
        setSadPlaylist((prev) => ({ ...prev, url: prev.songs[0]?.url }));
        break;
      case "study":
        setStudyPlaylist((prev) => ({ ...prev, url: prev.songs[0]?.url }));
        break;
      case "chill":
        setChillPlaylist((prev) => ({ ...prev, url: prev.songs[0]?.url }));
        break;
      default:
        console.log("Unknown genre:", genre);
    }
  };

  useEffect(() => {
    const genres = [
      "pop",
      "rock",
      "jazz",
      "house",
      "happy",
      "sad",
      "study",
      "chill",
    ];
    genres.forEach((genre) => {
      getSongsByGenre(genre).then((songs) => {
        const setStateFunc = {
          pop: setPopPlaylist,
          rock: setRockPlaylist,
          jazz: setJazzPlaylist,
          house: setHousePlaylist,
          happy: setHappyPlaylist,
          sad: setSadPlaylist,
          study: setStudyPlaylist,
          chill: setChillPlaylist,
        }[genre];

        setStateFunc({ songs });
        playlistUrl(genre);
      });
    });
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
        <LeftBar
          playlists={playlists}
          setCurrentPlaylistInfo={setCurrentPlaylistInfo}
          setCurrentPlace={setCurrentPlace}
        />

        {currentPlace === "main" && (
          <MainMiddle
            setCurrentPlace={setCurrentPlace}
            setCurrentBottomSong={setCurrentBottomSong}
            popPlaylist={popPlaylist}
            rockPlaylist={rockPlaylist}
            jazzPlaylist={jazzPlaylist}
            housePlaylist={housePlaylist}
            happyPlaylist={happyPlaylist}
            sadPlaylist={sadPlaylist}
            studyPlaylist={studyPlaylist}
            chillPlaylist={chillPlaylist}
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

        {currentPlace === "database" && (
          <DatabaseMiddle
            setCurrentBottomSong={setCurrentBottomSong}
          ></DatabaseMiddle>
        )}

        {currentPlace === "playlist" && (
          <PlaylistMiddle
            setCurrentBottomSong={setCurrentBottomSong}
            playlistInfo={currentPlaylistInfo}
          />
        )}
        {currentPlace === "lyrc" && (
          <LyrcsMiddle song={currentBottomSong}></LyrcsMiddle>
        )}

        <FriendActivity
          friendsData={friendsData}
          setCurrentPlace={setCurrentPlace}
        />
        {currentPlace === "friend" && (
          <FriendProfileMiddle></FriendProfileMiddle>
        )}
        <BottomBar song={currentBottomSong} setCurrentPlace={setCurrentPlace} />
      </div>
    </>
  );
};
export default MainPage;
