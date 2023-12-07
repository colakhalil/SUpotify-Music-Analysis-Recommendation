import React from "react";
import "../pagesCSS/PlaylistMiddle.css";
import PlaylistPicture from "./PlaylistPicture";
import PlaylistName from "./subcomponents/PlaylistName";
import PlaylistContainer from "./subcomponents/PlaylistContainer";

const PlaylistMiddle = ({setCurrentBottomSong ,playlistInfo}) => {
  console.log('playlistInfo:', playlistInfo); 
  return (
    <div className="playlist-middle">
      <PlaylistPicture imageUrl="https://cdn.mos.cms.futurecdn.net/oCtbBypcUdNkomXw7Ryrtf-650-80.jpg.webp" />
      <PlaylistName name={playlistInfo.name} />
      <PlaylistContainer songs={playlistInfo.songs} setCurrentBottomSong={setCurrentBottomSong} />
    </div>
    
    
    
  );
}; 
export default PlaylistMiddle;

