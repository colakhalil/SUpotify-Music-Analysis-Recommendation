
import React from 'react';
import '../../pagesCSS/UserPart.css';

const UserPart = ({ userData }) => {
    return (
      <div className="user-part-container">
        <div className="user-profile">
          <img
            className="user-profile-picture"
            src={userData.profilePicture}
            alt={`${userData.username}'s profile`}
          />
          <div className="user-info">
            <h1 className="user-username">{userData.username}</h1>
            <p className="user-friend-count">{userData.friendCount} Friends</p>
          </div>
        </div>
      </div>
    );
  };
  
  export default UserPart;