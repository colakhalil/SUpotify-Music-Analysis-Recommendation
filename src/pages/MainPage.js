import React, { useState, useEffect } from "react";
import "../pagesCSS/MainPage.css";
import "../pagesCSS/LeftBar.css";
import "../pagesCSS/FriendBar.css";
import "../pagesCSS/BottomBar.css";




import Searched from "../components/Searched";
import axios from "axios";
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
import globalVar from "../global";

const MainPage = () => {
  const [currentPlace, setCurrentPlace] = useState("main");
  const [searchedarray, setSearchedArray] = useState({});
  const [currentPlaylistInfo, setCurrentPlaylistInfo] = useState(null);
  const [dataBaseChanged, setDataBaseChanged] = useState(false);
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
    userPrevRating: 0,
    userPrevRatingArtist: 0,
    userPrevRatingAlbum: 0,
    artist_id: "artist_id",
    album_id: "album_id",
  }); // Initialize with an empty object or initial song data

  // ... [other functions and states]

  const formatDuration = (durationMs) => {
    const minutes = Math.floor(durationMs / 60000);
    const seconds = ((durationMs % 60000) / 1000).toFixed(0);
    return `${minutes}:${seconds < 10 ? "0" : ""}${seconds}`;
  };
  useEffect(() => {
    const fetchData = async () => {
      try {
        // Use your specific API endpoint
        const apiEndpoint = "http://127.0.0.1:8008/user_data/" + globalVar.mail;

        const response = await axios.get(apiEndpoint);
        let song_id = response.data.lastListenedSong;
        if (song_id != null) {
          try {
            const response = await fetch(
              `http://127.0.0.1:8008/get_song_info/` +
                globalVar.username +
                `/` +
                song_id
            );
            if (!response.ok) {
              throw new Error(`HTTP error! status: ${response.status}`);
            }
            let songData = await response.json();
            if (songData.song_id !== undefined) {
              songData.id = songData.song_id;
              delete songData.song_id;
            }
            // Format the duration
            if (songData.duration) {
              songData = {
                ...songData,
                duration: formatDuration(songData.duration),
              };
            }

            // Format the artists array
            if (songData.artists && Array.isArray(songData.artists)) {
              songData = {
                ...songData,
                artists: songData.artists.join(" "),
              };
            }

            setCurrentBottomSong(songData);
          } catch (error) {
            console.error("Error fetching song data:", error);
          }
        }
        // You can continue your logic here with the song_id value
      } catch (error) {
        console.error("API request error:", error);
      }
    };

    fetchData();
  }, []);
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
        `http://127.0.0.1:8008/rrecommendations/${genre}`
      );
      if (!response.ok) {
        throw new Error(
          `HTTP error! status:SIKINTI YOK LINK YANLIS ${response.status}`
        );
      }
      const data = await response.json();

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
  const [friendsData, setFriendsData] = useState([
    {
      name: "ezgi",
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
  ]);
  const [friendsUpdate, setFriendsUpdate] = useState(false); // State to trigger friends data update
  // DUMMY DATALAR
  useEffect(() => {
    const fetchFriendsActivity = async () => {
      try {
        const response = await fetch(
          `http://127.0.0.1:8008/friends_activity/${globalVar.username}`
        );
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();

        for (let i = 0; i < data.length; i++) {
          if (
            data[i].lastListenedSong != null &&
            data[i].lastListenedSong != "private"
          ) {
            try {
              const response = await fetch(
                `http://127.0.0.1:8008/get_song_info/` +
                  globalVar.username +
                  `/` +
                  data[i].lastListenedSong
              );
              if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
              }
              let songData = await response.json();
              if (songData.song_id !== undefined) {
                songData.id = songData.song_id;
                delete songData.song_id;
              }
              // Format the duration
              if (songData.duration) {
                songData = {
                  ...songData,
                  duration: formatDuration(songData.duration),
                };
              }

              // Format the artists array
              if (songData.artists && Array.isArray(songData.artists)) {
                songData = {
                  ...songData,
                  artists: songData.artists.join(" "),
                };
              }

              data[i].lastListenedSong =
                songData.title + " " + songData.artists;
            } catch (error) {
              console.error("Error fetching song data:", error);
            }
          }
        }

        setFriendsData(data);
      } catch (error) {
        console.error("Error fetching friends activity:", error);
      }
    };

    fetchFriendsActivity();
  }, [friendsUpdate]); // Depend on friendsUpdate to refetch when it changes

  return (
    <>
      <div className="main-container">
        <LeftBar
          setCurrentPlaylistInfo={setCurrentPlaylistInfo}
          setCurrentPlace={setCurrentPlace}
        />

        {currentPlace === "main" && (
          <MainMiddle
            friendsUpdate={friendsUpdate}
            setCurrentPlace={setCurrentPlace}
            friendsData={friendsData}
            setCurrentBottomSong={setCurrentBottomSong}
            setSearchedArray={setSearchedArray}
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
          <ProfileMiddle setCurrentPlace={setCurrentPlace}></ProfileMiddle>
        )}

        {currentPlace === "database" && (
          <DatabaseMiddle
            setCurrentBottomSong={setCurrentBottomSong}
            dataBaseChanged={dataBaseChanged}
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
          friendsUpdate={friendsUpdate}
          setFriendsUpdate={setFriendsUpdate}
          friendsData={friendsData}
          setCurrentPlace={setCurrentPlace}
        />
        {currentPlace === "friend" && (
          <FriendProfileMiddle></FriendProfileMiddle>
        )}
        {currentPlace === "searched" && (
          <Searched
            users={searchedarray}
            setFriendsUpdate={setFriendsUpdate}
            friendsUpdate={friendsUpdate}
            friendsData={friendsData}
          ></Searched>
        )}
        <BottomBar
          song={currentBottomSong}
          setSong={setCurrentBottomSong}
          setCurrentPlace={setCurrentPlace}
          setDataBaseChanged={setDataBaseChanged}
          dataBaseChanged={dataBaseChanged}
        />
      </div>
    </>
  );
};
export default MainPage;
