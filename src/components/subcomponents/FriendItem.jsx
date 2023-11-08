import React from 'react';

const FriendItem = ({ friend }) => {
  return (
    <div className="friend" key={friend.name}>
      <img
        src={friend.profilePicture}
        alt={`${friend.name}'s profile`}
        className="friend-picture"
      />
      <div className="friend-info">
        <p className="friend-name">{friend.name}</p>
        <p className="last-song">{friend.lastListenedSong}</p>
      </div>
    </div>
  );
};

export default FriendItem;
