import React from "react";
import globalVar from "../../global.js";

const PlaylistContainer = ({ songs, setCurrentBottomSong }) => {
  console.log("ihtiyacım olan", songs);
  const handleSongClick = async (song) => {
    console.log("Song: " + song.id + " clicked");

    try {
      const response = await fetch(
        `http://127.0.0.1:8008/get_song_info/` +
          globalVar.username +
          `/` +
          song.id
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
        <div className="song-duration-h">Album ID</div>
      </div>
      {songs.map((song, index) => (
        <div
          className="song-row"
          key={song.id || index}
          onClick={() => handleSongClick(song)}
        >
          <div className="song-index">{index + 1}</div>
          <div className="song-title-row">{song.songName}</div>
          <div className="song-artist">
            {Array.isArray(song.artistName)
              ? song.artistName.join(" ")
              : song.artistName}
          </div>

          <div className="song-duration">{formatDuration(song.songLength)}</div>
        </div>
      ))}
    </div>
  );
};

export default PlaylistContainer;
