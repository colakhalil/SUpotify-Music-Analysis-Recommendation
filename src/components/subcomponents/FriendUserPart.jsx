import React from 'react';
import '../../pagesCSS/FriendProfile.css';

const FriendUserPart = ({ friendData }) => {
  if (!friendData) return null;

  const altText = `${friendData.friendName}'s profile`;
  const profilePicture = friendData.profilePicture || "default-profile-pic-url.jpg"; // Add a default profile picture URL

  const handleAddFriend = () => {
    console.log("Add friend clicked");
    // Further logic to add a friend
  };

  const handleRemoveFriend = () => {
    console.log("Remove friend clicked");
    // Further logic to remove a friend
  };

  return (
    <div className="user-part-container">
      <div className="user-profile">
        <img className="user-profile-picture" src={profilePicture} alt={altText} />
        <div className="user-info">
          <h1 className="user-username">{friendData.friendName}</h1>
          <div className="friend-count-and-actions">
            {friendData.numberOfFriends !== undefined && (
              <>
                <p className="user-friend-count">
                  {friendData.numberOfFriends} {friendData.numberOfFriends === 1 ? 'Friend' : 'Friends'}
                </p>
                <div class='buttons'>
                    <button onClick={handleAddFriend}>Add Friend</button>
                    <button onClick={handleRemoveFriend}>Remove Friend</button>
                </div>


              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default FriendUserPart;
