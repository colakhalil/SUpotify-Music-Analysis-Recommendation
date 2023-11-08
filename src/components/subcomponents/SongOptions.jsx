import React from 'react';

const SongOptions = ({ toggleLyrics }) => {
  return (
    <button className="song-lyrics-btn" onClick={toggleLyrics}>
      Lyrics
    </button>
  );
};

export default SongOptions;
