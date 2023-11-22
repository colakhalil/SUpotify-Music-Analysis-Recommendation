import React from 'react';
import '../../pagesCSS/UserPart.css';


const UserPart = ({ userData }) => {
  if (!userData) return null;

  const altText = `${userData.username}'s profile`;
  const profilePicture = userData.profilePicture || "default-profile-pic-url.jpg"; // Add a default profile picture URL

  return (
    <div className="user-part-container">
      <div className="user-profile">
        <img className="user-profile-picture" src={profilePicture} alt={altText} />
        <div className="user-info">
          <h1 className="user-username">{userData.username}</h1>
          {userData.friendsCount !== undefined && (
            <p className="user-friend-count">
              {userData.friendsCount} {userData.friendsCount === 1 ? 'Friend' : 'Friends'}
            </p>
          )}
        </div>
      </div>
    </div>
  );
};

export default UserPart;