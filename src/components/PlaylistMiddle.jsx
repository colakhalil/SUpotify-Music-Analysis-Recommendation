import React from 'react';
import "../pagesCSS/PlaylistMiddle.css";
import PlaylistPicture from './PlaylistPicture';
import PlaylistName from './subcomponents/PlaylistName';
import PlaylistContainer from './subcomponents/PlaylistContainer';

const PlaylistMiddle = ({ playlistData }) => {
  return (
    <div className="playlist-middle">
      <PlaylistPicture imageUrl={playlistData.playlistPicture} />
      <PlaylistName name={playlistData.playlistName} />
      <PlaylistContainer songs={playlistData.songs} />
    </div>
  );
};

export default PlaylistMiddle;
