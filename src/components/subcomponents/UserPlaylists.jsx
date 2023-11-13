// UserPlaylists.js
import React from 'react';
import '../../pagesCSS/UserPlaylists.css';

const UserPlaylists = ({ playlists }) => {
  return (
    <div className="user-playlists-container">
      <h2>User’s Playlists</h2>
      <div className="playlists">
        {playlists.map((playlist, index) => (
          <div key={index} className="playlist-card">
            <div className="playlist-thumbnail" style={{ backgroundImage: `url(${playlist.thumbnail})` }}></div>
            <p className="playlist-name">{playlist.name}</p>
            {/* Burada playlist'in diğer özelliklerini ekleyebilirsiniz */}
          </div>
        ))}
      </div>
    </div>
  );
};

export default UserPlaylists;
