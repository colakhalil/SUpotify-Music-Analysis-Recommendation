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
  const [showMergeForm, setShowMergeForm] = useState(false); // State to control the visibility of the merge form
  const [userPlaylists, setUserPlaylists] = useState([]); // State to store the user's playlists


  useEffect(() => {
    // Update the key whenever playlistInfo changes to force a re-render
    setKey((prevKey) => prevKey + 1);
  }, [playlistInfo]);

  // Add this useEffect hook to fetch playlists when the merge form is shown
useEffect(() => {
  if (showMergeForm) {
    const fetchUserPlaylists = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8008/get_user_playlists');
        setUserPlaylists(response.data);
      } catch (error) {
        console.error('Error fetching user playlists:', error);
      }
    };

    fetchUserPlaylists();
  }
}, [showMergeForm]);


// Function to merge the selected playlist with the current playlist
const mergePlaylist = async (clickedPlaylistID) => {
  const currentPlaylistID = playlistInfo.playlistID; // Replace with your current playlist ID

  try {
    const response = await axios.get(`http://127.0.0.1:8008/get_playlists_songs/${currentPlaylistID}/${clickedPlaylistID}`);
    const mergedSongsData = response.data.map(song => ({
      id: song.song_id, // Make sure the id property is named correctly
      songName: song.song_name,
      artistName: song.artist_name,
      songLength: song.songLength, // This should be in milliseconds
      url: song.picture, // The url for the song's image
    }));

    setSongs((prevSongs) => {
      // Merge the songs avoiding duplicates
      const mergedSongs = [...prevSongs, ...mergedSongsData.filter((newSong) => !prevSongs.some((song) => song.id === newSong.id))];
      return mergedSongs;
    });

    setShowMergeForm(false); // Close the merge form
  } catch (error) {
    console.error('Error merging playlists:', error);
  }
};



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
        <div className="button-container">
          {/* Conditional rendering based on `isEnrichAllowed` */}
          {playlistInfo.isEnrichAllowed && (
            <button className="button-shared enrich-button" onClick={enrichPlaylist}>
              Enrich
            </button>
          )}
      
          <button className="button-shared merge-button" onClick={() => setShowMergeForm(true)}>
            Merge
          </button>
          
        </div>

        
        {showMergeForm && (
          <div className="merge-form">
            <div className="merge-form-header">
              <button className="button-shared back-button" onClick={() => setShowMergeForm(false)}>
                Back
              </button>
            </div>
            <div className="merge-playlist-container">
              {userPlaylists.map((playlist) => (
                <div key={playlist.playlistID} onClick={() => mergePlaylist(playlist.playlistID)} className="playlist-entry">
                  {playlist.name} - {playlist.songNumber} songs
                </div>
              ))}
            </div>
          </div>
        )}

        <PlaylistContainer
          songs={songs}
          setCurrentBottomSong={setCurrentBottomSong}
        />
      </div>
    </div>
  );
}; 
export default PlaylistMiddle;

