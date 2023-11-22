import React from 'react';

const FriendItem = ({ friend , setCurrentPlace}) => {
  const handleFriendProfile = ({friend}) => {
    console.log("You clicked on friend");
    setCurrentPlace("friend");
    // Implement your playlist click functionality here
    console.log(friend)
  };
  return (
    <div 
      className="friend" 
      key={friend.name} 
      onClick={() => handleFriendProfile(friend, setCurrentPlace)}
      style={{ cursor: 'pointer' }} // Add cursor style for better UX
    >
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
