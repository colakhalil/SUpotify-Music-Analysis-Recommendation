import React, { useState, useEffect } from "react";
import SongDetails from "./subcomponents/SongDetails";
import SongControls from "./subcomponents/SongControls";
import SongRating from "./subcomponents/SongRating";
import globalVar from "../global.js";

import SongDetailsExtra from "./subcomponents/SongDetailsExtra";

const RatingPopup = ({ isOpen, onClose, song, userRating, onRate }) => {
  if (!isOpen) return null;

  // You can add your rating logic here
  const handleRating = (rating) => {
    onRate(rating);
    onClose(); // Close the popup after rating
  };

  return (
    <div className="popup-overlay">
      <div className="popup-content">
        <h3>Rate the Song</h3>
        <SongRating
          song={song}
          userRating={userRating}
          onRatingChange={handleRating}
        />
        <button onClick={onClose}>Close</button>
      </div>
    </div>
  );
};

const RatingPopupAlbum = ({ isOpen, onClose, song, userRating, onRate }) => {
  if (!isOpen) return null;

  // You can add your rating logic here
  const handleRating = (rating) => {
    console.log("Rating given: ", rating);
    onRate(rating);
    onClose(); // Close the popup after rating
  };

  return (
    <div className="popup-overlay">
      <div className="popup-content">
        <h3>Rate the Album</h3>
        <SongRating
          song={song}
          userRating={userRating}
          onRatingChange={handleRating}
        />
        <button onClick={onClose}>Close</button>
      </div>
    </div>
  );
};

const RatingPopupArtist = ({ isOpen, onClose, song, userRating, onRate }) => {
  if (!isOpen) return null;

  // You can add your rating logic here
  const handleRating = (rating) => {
    console.log("Rating given: ", rating);
    onRate(rating);
    onClose(); // Close the popup after rating
  };

  return (
    <div className="popup-overlay">
      <div className="popup-content">
        <h3>Rate the Artist</h3>
        <SongRating
          song={song}
          userRating={userRating}
          onRatingChange={handleRating}
        />
        <button onClick={onClose}>Close</button>
      </div>
    </div>
  );
};

const BottomBar = ({ song, setCurrentPlace, currentPlace, setSong }) => {
  console.log("Song: ", song);
  const [isSongRatePopupOpen, setIsSongRatePopupOpen] = useState(false); //songrate
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [isDeleted, setIsDeleted] = useState(false);
  const [isPopupOpen, setIsPopupOpen] = useState(false);
  const [isAlbumRatePopupOpen, setIsAlbumRatePopupOpen] = useState(false);

  const handleOpenPopup = () => {
    setIsPopupOpen(true);
  };

  const handleClosePopup = () => {
    setIsPopupOpen(false);
  };

  const handleOpenSongRatePopup = () => {
    setIsSongRatePopupOpen(true);
  };

  // Function to close song rating popup
  const handleCloseSongRatePopup = () => {
    setIsSongRatePopupOpen(false);
  };

  const handleOpenAlbumRatePopup = () => {
    setIsAlbumRatePopupOpen(true);
  };

  // Function to close album rating popup
  const handleCloseAlbumRatePopup = () => {
    setIsAlbumRatePopupOpen(false);
  };

  const handleDelete = async () => {
    if (isDeleted) {
      return; // Prevent further action if already clicked
    }

    try {
      const response = await fetch("/delete-song", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ song }),
      });

      if (response.ok) {
        console.log("Song deleted successfully");
        setIsDeleted(true); // Update state to reflect deletion
      } else {
        console.error("Failed to delete the song");
      }
    } catch (error) {
      console.error("Error:", error);
    }
  };

  const handleSong = async (newRating) => {
    console.log("NEW RATING: song ", newRating);
    setSong({ ...song, userPrevRating: newRating });

    const myjson = {
      song_id: song.id,
      rating: newRating,
      user_id: globalVar.username,
    };
    console.log("myjson: ", myjson);
    try {
      const response = await fetch("http://127.0.0.1:8008/change_rating_song", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(myjson),
      });

      const responseData = await response.json();

      if (response.ok) {
        // Handle the response if the request was successful
        console.log("Rating updated successfully", responseData);
      } else {
        // Handle errors if the request was unsuccessful
        console.error("Error updating rating", responseData);
      }
    } catch (error) {
      // Handle network errors
      console.error("Network error:", error);
    }

    // Add additional logic for when the rating changes
  };

  const handleAlbum = (newRating) => {
    console.log("NEW RATING: album", newRating);

    // Assuming the albumId is a string and you need the first part
    let albumId = song.album_id;
    // Update the song state or other logic here
    setSong({ ...song, userPrevRatingAlbum: newRating });

    // Define the data to be sent
    const data = {
      album_id: albumId,
      user_id: globalVar.username,
      rating: newRating,
    };

    // Send the POST request
    fetch("http://127.0.0.1:8008/change_rating_album", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Success:", data);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  };

  const handleArtist = (newRating) => {
    let userId = globalVar.username;
    let artistId = song.artist_id;

    console.log("NEW RATING: artist", newRating);

    // Update the song state or other logic here
    setSong({ ...song, userPrevRatingArtist: newRating });

    // Define the data to be sent
    const data = {
      artist_id: artistId,
      user_id: userId,
      rating: newRating,
    };

    // Send the POST request
    fetch("http://127.0.0.1:8008/change_rating_artist", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Success:", data);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  };

  const togglePlay = () => {
    setIsPlaying(!isPlaying);
    // Add additional logic for when play/pause is toggled
  };

  const toggleLyrics = () => {
    console.log("Lyrics toggled");
    setCurrentPlace("lyrc");

    // Add additional logic for when lyrics are toggled
  };

  const getSecondsFromDuration = (duration) => {
    const [minutes, seconds] = duration.split(":").map(Number);
    return minutes * 60 + seconds;
  };

  const songDurationInSeconds = getSecondsFromDuration(song.duration);

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

  useEffect(() => {
    if (currentTime >= songDurationInSeconds) {
      setIsPlaying(false);
      setCurrentTime(0);
    }
  }, [currentTime, songDurationInSeconds]);

  return (
    <div className="song-bar">
      <SongDetails song={song} />
      <SongControls
        isPlaying={isPlaying}
        togglePlay={togglePlay}
        currentTime={currentTime}
        songDurationInSeconds={songDurationInSeconds}
        song={song}
        toggleLyrics={toggleLyrics}
      />

      <button className="rate-btn" onClick={handleOpenSongRatePopup}>
        Song Rate
      </button>
      <button className="rate-btn" onClick={handleOpenPopup}>
        Artist Rate
      </button>
      <button className="rate-btn" onClick={handleOpenAlbumRatePopup}>
        Album Rate
      </button>
      <button
        className="delete-btn"
        onClick={handleDelete}
        disabled={isDeleted}
      >
        Delete
      </button>
      <SongDetailsExtra song={song} />
      <RatingPopupArtist
        isOpen={isPopupOpen}
        onClose={handleClosePopup}
        song={song}
        userRating={song.userPrevRatingArtist}
        onRate={handleArtist}
      />
      <RatingPopup
        isOpen={isSongRatePopupOpen}
        onClose={handleCloseSongRatePopup}
        song={song}
        userRating={song.userPrevRating}
        onRate={handleSong} // You can modify this if you have a different rating logic for songs
      />
      <RatingPopupAlbum
        isOpen={isAlbumRatePopupOpen}
        onClose={handleCloseAlbumRatePopup}
        userRating={song.userPrevRatingAlbum}
        onRate={handleAlbum}
      />
    </div>
  );
};

export default BottomBar;
