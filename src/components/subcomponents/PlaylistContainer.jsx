import React from "react";

const PlaylistContainer = ({ songs, setCurrentBottomSong }) => {
  const handleSongClick = async (song) => {
    console.log("Song: " + song.id + " clicked");

    try {
      const response = await fetch(
        `http://127.0.0.1:8008/get_song_info/Ezgi/${song.id}`
      );
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      let songData = await response.json();

      // Format the duration
      if (songData.duration) {
        songData = {
          ...songData,
          duration: formatDuration(songData.duration),
        };
      }

      setCurrentBottomSong(songData);
    } catch (error) {
      console.error("Error fetching song data:", error);
    }
  };

  // Helper function to format song duration from milliseconds to "mm:ss"
  const formatDuration = (durationMs) => {
    const minutes = Math.floor(durationMs / 60000);
    const seconds = ((durationMs % 60000) / 1000).toFixed(0);
    return `${minutes}:${seconds < 10 ? "0" : ""}${seconds}`;
  };

  // Helper function to format song rating (e.g., out of 10)
  const formatRating = (rating) => {
    return `${rating}/10`;
  };

  return (
    <div className="playlist-container">
      <div className="song-row header">
        <div className="song-index-h">#</div>
        <div className="song-title-h">Title</div>
        <div className="song-artist-h">Artist</div>
        <div className="song-duration-h">Duration</div>
        <div className="song-release-year-h">Release Year</div>
        <div className="song-rating-h">Rating</div>
      </div>
      {songs.map((song, index) => (
        <div
          className="song-row"
          key={song.id || index}
          onClick={() => handleSongClick(song)}
        >
          <div className="song-index">{index + 1}</div>
          <div className="song-title-row">{song.songName}</div>
          <div className="song-artist">{song.artistName}</div>
          <div className="song-duration">{formatDuration(song.songLength)}</div>
          <div className="song-release-year-p">{song.releaseYear}</div>
          <div className="song-rating-p">{formatRating(song.rating)}</div>
        </div>
      ))}
    </div>
  );
};

export default PlaylistContainer;
