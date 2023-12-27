import React, { useState } from 'react';
import EnrichButton from './EnrichButton'; // Make sure the path is correct

function PlaylistforEnrich({ userId, genre }) {
  const [songs, setSongs] = useState([]);

  const handleEnrich = (newSongs) => {
    // This function will be passed to EnrichButton and is called with the new songs
    setSongs((prevSongs) => [...prevSongs, ...newSongs]);
  };

  return (
    <div>
      {/* Pass the actual userId and genre to the EnrichButton */}
      <EnrichButton userId={userId} genre={genre} onEnrich={handleEnrich} />
      <ul>
        {songs.map((song) => (
          <li key={song.song_id}>
            {song.song_name} - {song.artist_name.join(', ')}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default PlaylistforEnrich;
