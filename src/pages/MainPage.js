import React, { useState, useEffect } from "react";
import "../pagesCSS/MainPage.css";
import Rating from "react-rating-stars-component";

const MainPage = () => {
  // Define the expanded song object
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
  // when song is updated this BottomBar also will be updated automatically
  return (
    <>
      <BottomBar song={song} />
      <FriendBar friendsData={friendsData} />
      <LeftBar playlists={playlists} />
    </>
  );
};

const BottomBar = ({ song }) => {
  const [userRating, setUserRating] = useState(song.userPrevRating);

  // Function to handle when the user changes their rating
  const handleRatingChange = (newRating) => {
    setUserRating(newRating);
    console.log("NEW RATING: ", newRating);

    // REQUEST!!!!!!! USER WILL CHANGE RATING ON THE SONG
  };

  // State hooks
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);

  // Convert song duration to seconds
  const getSecondsFromDuration = (duration) => {
    const [minutes, seconds] = duration.split(":").map(Number);
    return minutes * 60 + seconds;
  };

  const songDurationInSeconds = getSecondsFromDuration(song.duration);

  // Effect hook to handle the interval
  useEffect(() => {
    let interval;
    if (isPlaying) {
      interval = setInterval(() => {
        setCurrentTime((currentTime) => {
          const newTime = currentTime + 1;
          if (newTime >= songDurationInSeconds) {
            setIsPlaying(false);
            return songDurationInSeconds;
          }
          return newTime;
        });
      }, 1000);
    }
    return () => clearInterval(interval);
  }, [isPlaying, songDurationInSeconds]);

  // Toggle play/pause
  const togglePlay = () => {
    setIsPlaying(!isPlaying);
    // REQUEST!!!!!!!  USER'S LAST CLICKED SONG WILL BE CHANGED
  };

  // This will reset the timer and stop playing when the song duration is reached
  useEffect(() => {
    if (currentTime >= songDurationInSeconds) {
      setIsPlaying(false);
      setCurrentTime(0);
    }
  }, [currentTime, songDurationInSeconds]);

  // Function to toggle lyrics visibility
  const toggleLyrics = () => {
    //LYRCS WILL BE OPENED IN THE MAIN
    console.log("lyrcs");
  };

  return (
    <div className="song-bar">
      <div className="song-info">
        <img src={song.img} alt="album cover" className="album-cover" />
        <div className="firstInfo">
          <p className="song-title">{song.title}</p>
          <p className="song-artist">{song.artist}</p>
        </div>
        <div className="secondInfo" style={{ marginLeft: "2rem" }}>
          <p className="song-meta">Genre: {song.genre}</p>
          <p className="song-meta">Mood: {song.mood}</p>
          <p className="song-meta">Recording: {song.recordingType}</p>
        </div>

        <Rating
          count={5}
          value={userRating}
          size={24}
          activeColor="#ffd700" // Color for filled stars
          onChange={handleRatingChange}
        />
        <button
          className="song-lyrics-btn"
          onClick={toggleLyrics}
          style={{
            marginLeft: "2rem",
            padding: "10px 20px",

            border: "none",
            borderRadius: "5px",
            cursor: "pointer",
            boxShadow: "0px 4px 6px rgba(0, 0, 0, 0.1)",
            transition: "background-color 0.3s ease-in-out",
          }}
        >
          Lyrics
        </button>
      </div>
      <div className="song-controls">
        <button className="play-btn" onClick={togglePlay}>
          {isPlaying ? "Pause" : "Play"}
        </button>
        <div className="song-progress">
          <input
            type="range"
            min="0"
            max={songDurationInSeconds}
            value={currentTime}
            className="slider"
            readOnly
          />
          <div className="song-timer">
            {Math.floor(currentTime / 60)}:
            {String(currentTime % 60).padStart(2, "0")} / {song.duration}
          </div>
          <div className="thirdInfo" style={{ marginLeft: "1rem" }}>
            <p className="song-meta">Instruments: {song.instruments}</p>
            <p className="song-meta">Plays: {song.playCount}</p>
          </div>
          <div className="fourthInfo" style={{ marginLeft: "2rem" }}>
            <p className="song-meta">Released: {song.releaseYear}</p>
            <p className="song-meta">Added: {song.dateAdded}</p>
          </div>
        </div>
      </div>
      <div className="song-options">
        {/* Add any additional buttons or options here */}
      </div>
    </div>
  );
};

const FriendBar = ({ friendsData }) => {
  return (
    <div className="friend-bar">
      {friendsData.map((friend, index) => (
        <div className="friend" key={index}>
          <img
            src={friend.profilePicture}
            alt={friend.name}
            className="friend-picture"
          />
          <div className="friend-info">
            <p className="friend-name">{friend.name}</p>
            <p className="last-song">{friend.lastListenedSong}</p>
          </div>
        </div>
      ))}
    </div>
  );
};
const LeftBar = ({ playlists }) => {
  const handleClick = (playlistName) => {
    // Here you can handle the navigation or any other interaction
    console.log(`You clicked on ${playlistName}`);
    //REQUEST PLAYLIST SONGS SHOULD BE SEEN IN THE MAIN
  };
  const handleMain = () => {
    // Here you can handle the navigation or any other interaction
    //REQUEST USER SHOULD NAVIGATE TO MAIN
  };
  const handleSearch = () => {
    // Here you can handle the navigation or any other interaction
    //REQUEST USER SHOULD NAVIGATE TO SEARCH
  };

  return (
    <div className="left-bar">
      <button className="left-bar-button" onClick={handleMain}>
        Ana sayfa
      </button>
      <button className="left-bar-button" onClick={handleSearch}>
        Ara
      </button>
      <button className="left-bar-button">Kitaplığın</button>

      <div className="playlists">
        {playlists.map((playlist, index) => (
          <button
            key={index}
            className="playlist-button"
            onClick={() => handleClick(playlist.playlist_name)}
          >
            <img
              src={playlist.playlist_picture}
              alt={playlist.playlist_name}
              className="playlist-image"
            />
            <div className="playlist-info">
              <div className="playlist-name">{playlist.playlist_name}</div>
              <div className="song-number">{playlist.song_number} songs</div>
            </div>
          </button>
        ))}
      </div>
    </div>
  );
};

export default MainPage;
