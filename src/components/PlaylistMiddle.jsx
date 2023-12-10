import React from "react";
import "../pagesCSS/PlaylistMiddle.css";
import PlaylistPicture from "./PlaylistPicture";
import PlaylistName from "./subcomponents/PlaylistName";
import PlaylistContainer from "./subcomponents/PlaylistContainer";
import { useEffect, useState } from "react";
const PlaylistMiddle = ({ setCurrentBottomSong, playlistInfo }) => {
  const [key, setKey] = useState(0);
  useEffect(() => {
    // Update the key whenever playlistInfo changes to force a re-render
    setKey((prevKey) => prevKey + 1);
  }, [playlistInfo]);
  return (
    <div className="playlist-middle" key={key}>
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
