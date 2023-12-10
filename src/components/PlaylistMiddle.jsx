import React from "react";
import "../pagesCSS/PlaylistMiddle.css";
import PlaylistPicture from "./PlaylistPicture";
import PlaylistName from "./subcomponents/PlaylistName";
import PlaylistContainer from "./subcomponents/PlaylistContainer";

const PlaylistMiddle = ({ setCurrentBottomSong, playlistInfo }) => {
  return (
    <div className="playlist-middle">
      <PlaylistPicture imageUrl={playlistInfo.url} />
      <PlaylistName name={playlistInfo.name} />
      <PlaylistContainer
        songs={playlistInfo.songs}
        setCurrentBottomSong={setCurrentBottomSong}
      />
    </div>
  );
}; 
export default PlaylistMiddle;

