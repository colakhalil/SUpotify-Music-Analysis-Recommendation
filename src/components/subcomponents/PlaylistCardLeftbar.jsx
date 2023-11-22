import React from "react";
import PlaylistItemLeftbar from "./PlaylistItemLeftbar";

const PlaylistCardLeftbar = ({ playlists, onPlaylistClick }) => {
  return (
    <div className="playlists">
      {playlists.map((playlist, index) => (
        <PlaylistItemLeftbar
          key={playlist.playlistID}
          playlist={playlist}
          onClick={onPlaylistClick}
        />
      ))}
    </div>
  );
};

export default PlaylistCardLeftbar;
