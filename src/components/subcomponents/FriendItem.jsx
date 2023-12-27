import React from 'react';

const FriendItem = ({ friend , onSelectFriend}) => {
  /*
  const handleFriendProfile = () => {
    console.log("You clicked on friend item:", friend.name);
    setCurrentPlace("friend");
    // Implement your playlist click functionality here
  };
*/
  const handleFriendProfile = () => {
    console.log("You clicked on friend item:", friend.name);
    onSelectFriend(friend.name); // Call the function passed from MainPage via FriendActivity
  };
  return (
    <div 
      className="friend" 
      key={friend.name} 
      onClick={handleFriendProfile}
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
