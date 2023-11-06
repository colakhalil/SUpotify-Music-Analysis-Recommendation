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

  // when song is updated this BottomBar also will be updated automatically
  return <BottomBar song={song} />;
};

const BottomBar = ({ song }) => {
  const [userRating, setUserRating] = useState(song.userPrevRating);

  // Function to handle when the user changes their rating
  const handleRatingChange = (newRating) => {
    setUserRating(newRating);

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
    // REQUEST!!!!!!!  LAST CLICKED SONG WILL BE CHANGED
    // REQUEST!!!!!!!  PLAYS NUMBER WILL BE INCREASED
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
          style={{ marginLeft: "2rem" }}
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
export default MainPage;
