import axios from 'axios';
import PlaylistPicture from "./PlaylistPicture";
import PlaylistName from "./subcomponents/PlaylistName";
import PlaylistContainer from "./subcomponents/PlaylistContainer";
import "../pagesCSS/PlaylistMiddle.css";
import globalVar from '../global';


import { useEffect, useState } from "react";
const PlaylistMiddle = ({ setCurrentBottomSong, playlistInfo }) => {
  const [key, setKey] = useState(0);
  const [songs, setSongs] = useState(playlistInfo.songs || []);
  const [enrichCount, setEnrichCount] = useState(0); // Counter to keep track of enrich clicks

  useEffect(() => {
    // Update the key whenever playlistInfo changes to force a re-render
    setKey((prevKey) => prevKey + 1);
  }, [playlistInfo]);


  const enrichPlaylist = async () => {
    console.log(`Enriching playlist for genre: ${playlistInfo.name}`); // Log the genre being enriched
    
    try {
      const response = await axios.get(`http://127.0.0.1:8008/enrich_rec/${globalVar.username}/${playlistInfo.name}`);
      console.log('Response from enrich:', response.data); // Log the raw response data
  
      if (response.status === 200 && response.data.length > 0) {
        // Get a new song based on the enrichCount
        const newSongIndex = enrichCount % response.data.length;
        const newSong = response.data[newSongIndex];
        console.log('New song to add:', newSong); // Log the new song to be added
  
        setSongs((prevSongs) => {
          // Check if the song is already in the playlist to avoid duplicates
          if (!prevSongs.some((song) => song.id === newSong.song_id)) {
            return [...prevSongs, {
              songName: newSong.song_name,
              artistName: newSong.artist_name.join(', '), // Join the artists array to form a string
              songLength: newSong.songLength,
              id: newSong.song_id,
              url: newSong.picture,
            }];
          }
          return prevSongs;
        });

        // Increment the enrich count
        setEnrichCount((prevCount) => prevCount + 1);
      }
    } catch (error) {
      console.error('Error fetching enriched playlist:', error);
    }
  };

  return (
    <div className="centerk">
      <div className="playlist-middle" key={key}>
        <PlaylistPicture className="center-photo" imageUrl={playlistInfo.url}/>
        <PlaylistName name={playlistInfo.name} className="center-name"/>
        <button className="enrich-button" onClick={enrichPlaylist}>Enrich</button>
        <PlaylistContainer
          songs={songs}
          setCurrentBottomSong={setCurrentBottomSong}
        />
      </div>
    </div>
  );
}; 
export default PlaylistMiddle;

