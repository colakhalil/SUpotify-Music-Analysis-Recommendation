import React from 'react';
import "../pagesCSS/PlaylistMiddle.css";
import PlaylistPicture from './PlaylistPicture';
import PlaylistName from './subcomponents/PlaylistName';
import PlaylistContainer from './subcomponents/PlaylistContainer';

const PlaylistMiddle = ({ playlistData,recommendedPop }) => {
  return (
    <div className="playlist-middle">
      <PlaylistPicture imageUrl={playlistData.playlistPicture} />
      <PlaylistName name={playlistData.playlistName} />
      <PlaylistContainer songs={recommendedPop.songs} />
    </div>
  );
};

export default PlaylistMiddle;
