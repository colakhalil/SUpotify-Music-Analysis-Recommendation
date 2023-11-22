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

  // DUMMY DATALAR
  const [playlistPop, setPlaylistPop] = useState({ songs: [] });
  const [recommendedPop, setRecommendedPop] = useState({ songs: [] }); // Initialize an empty recommendedPop object
  
  const fetchRecommendationsByGenre = (genre) => {
    fetch(`http://127.0.0.1:8008/recommendations/${genre}`)
      .then(response => response.json())
      .then(data => {
        const formattedSongs = data.tracks.map(track => ({
          songName: track.name,
          artistName: track.artists.map(artist => artist.name).join(', '),
          songLength: track.duration_ms,
          releaseYear: new Date(track.album.release_date).getFullYear(),
          rating: track.popularity,
          album: track.album.name,
          songPicture: track.album.images[0].url
        }));

        setPlaylistPop({ songs: formattedSongs });
        
        // Create the recommendedPop object inside the .then() block
        const recommendations = formattedSongs; // Assuming you want to use the same data for recommendedPop

        setRecommendedPop({ songs: recommendations });
      })
      .catch(error => console.error('Error fetching data:', error));
  };
  
  useEffect(() => {
    fetchRecommendationsByGenre("pop");
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
    title: "Beni Böyle Hatırla",
    artist: "Çetin Dilşiz",
    duration: "2:48",
    lyrics: [
      "Sessiz bir köşede her şeyden uzak",
      "Meçhul yarınlara terk edilmişim",
      "Dostluklar yalanmış sevgiler tuzakmış",
      "Tuzak",
      "Hayret yanılmışım yalnızım şimdi",
      "Oysa mutluluğu hayal etmiştim",
      "Gidenler unutmuş aşkları yalanmış",
      "Yalan",
      "Güneşin doğuşu batışı farksız",
      "Nasıl yaşanırsa yaşadım ben aşksız",
      "Güneşin doğuşu batışı farksız",
      "Nasıl yaşanırsa yaşadım ben aşksız",
      "Demir attım yalnızlığa",
      "Bir hasret denizinde",
      "Ve şimdi hayallerim o günlerin izinde",
      "Yüreğimde duygular ümitlerim nerede",
      "Demir attım yalnızlığa",
      "Bir hasret denizinde",
      "Ve şimdi hayallerim o günlerin izinde",
      "Yüreğimde duygular ümitlerim nerede",
      "Şöyle bir düşünüp her şeyi birden",
      "Neden anıları bitirmeyişim",
      "Yalanmış sevgiler kalbimden uzakmış",
      "Uzak",
      "Boşa beklemişim yollara bakıp",
      "Kurak topraklara umutlar ekmişim",
      "Arzular avuttu gördüğüm hayalmiş",
      "Hayal",
      "Güneşin doğuşu batışı farksız",
      "Nasıl yaşanırsa yaşadım ben aşksız",
      "Güneşin doğuşu batışı farksız",
      "Nasıl yaşanırsa yaşadım ben aşksız",
      "Demir attım yalnızlığa",
      "Bir hasret denizinde",
      "Ve şimdi hayallerim o günlerin izinde",
      "Yüreğimde duygular ümitlerim nerede",
      "Demir attım yalnızlığa",
      "Bir hasret denizinde",
      "Ve şimdi hayallerim o günlerin izinde",
      "Yüreğimde duygular ümitlerim nerede",

      // ... More lyrics lines
    ],
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
          <MainMiddle
            setCurrentPlace={setCurrentPlace}
          ></MainMiddle>
        )}
        {currentPlace === "submit-form" && (
          <SubmissionForm></SubmissionForm>
        )}
        {currentPlace === "submit-formE" && (
          <SubmissionFormExport></SubmissionFormExport>
        )}
        {currentPlace === "profile" && (
          <ProfileMiddle
            userData={userData}
            setCurrentPlace={setCurrentPlace}
          ></ProfileMiddle>
        )}
        {currentPlace === "lyrc" && <LyrcsMiddle song={song}></LyrcsMiddle>}
        {currentPlace === "playlist" && (
          <PlaylistMiddle playlistData={playlistData} recommendedPop= {recommendedPop}></PlaylistMiddle>
        )}
        <FriendActivity friendsData={friendsData} setCurrentPlace={setCurrentPlace}/>
        {currentPlace === "friend" && (
          <FriendProfileMiddle
          ></FriendProfileMiddle>
        )}
        <BottomBar song={song} setCurrentPlace={setCurrentPlace} />
      </div>
    </>
  );
};
export default MainPage;