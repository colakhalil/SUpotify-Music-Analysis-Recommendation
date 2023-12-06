import React, { useState, useEffect } from "react";
import SongDetails from "./subcomponents/SongDetails";
import SongControls from "./subcomponents/SongControls";
import SongRating from "./subcomponents/SongRating";
import SongOptions from "./subcomponents/SongOptions";
import SongDetailsExtra from "./subcomponents/SongDetailsExtra";



const RatingPopup = ({ isOpen, onClose, song, userRating, onRate }) => {
  if (!isOpen) return null;

  // You can add your rating logic here
  const handleRating = (rating) => {
    console.log('Rating given: ', rating);
    onRate(rating);
    onClose(); // Close the popup after rating
  };

  return (
    <div className="popup-overlay">
      <div className="popup-content">
        <h3>Rate the Song</h3>
        <SongRating song={song} userRating={userRating} onRatingChange={handleRating} />
        <button onClick={onClose}>Close</button>
      </div>
    </div>
  );
};

const RatingPopupAlbum = ({ isOpen, onClose, song, userRating, onRate }) => {
  if (!isOpen) return null;

  // You can add your rating logic here
  const handleRating = (rating) => {
    console.log('Rating given: ', rating);
    onRate(rating);
    onClose(); // Close the popup after rating
  };

  return (
    <div className="popup-overlay">
      <div className="popup-content">
        <h3>Rate the Album</h3>
        <SongRating song={song} userRating={userRating} onRatingChange={handleRating} />
        <button onClick={onClose}>Close</button>
      </div>
    </div>
  );
};

const RatingPopupArtist = ({ isOpen, onClose, song, userRating, onRate }) => {
  if (!isOpen) return null;

  // You can add your rating logic here
  const handleRating = (rating) => {
    console.log('Rating given: ', rating);
    onRate(rating);
    onClose(); // Close the popup after rating
  };

  return (
    <div className="popup-overlay">
      <div className="popup-content">
        <h3>Rate the Artist</h3>
        <SongRating song={song} userRating={userRating} onRatingChange={handleRating} />
        <button onClick={onClose}>Close</button>
      </div>
    </div>
  );
};

const BottomBar = ({ song, setCurrentPlace, currentPlace }) => {
  const [userRating, setUserRating] = useState(song.userPrevRating);
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
      const response = await fetch('/delete-song', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ song }),
      });

      if (response.ok) {
        console.log('Song deleted successfully');
        setIsDeleted(true); // Update state to reflect deletion
      } else {
        console.error('Failed to delete the song');
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const handleRatingChange = (newRating) => {
    setUserRating(newRating);
    console.log("NEW RATING: ", newRating);
    // Add additional logic for when the rating changes
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
        userRating={userRating}
        onRate={handleRatingChange}
      />
      <RatingPopup
        isOpen={isSongRatePopupOpen}
        onClose={handleCloseSongRatePopup}
        song={song}
        userRating={userRating}
        onRate={handleRatingChange} // You can modify this if you have a different rating logic for songs
      />
      <RatingPopupAlbum
        isOpen={isAlbumRatePopupOpen}
        onClose={handleCloseAlbumRatePopup}
        userRating={userRating}
        onRate={handleRatingChange}
      />
    </div>
  );
};

export default BottomBar;
