import React from "react";
import globalVar from "../global.js";

const UserList = ({ users, friendsData }) => {
  const checkIsFriend = (userId) => {
    return friendsData.some((friend) => friend.name === userId);
  };

  const onAddFriend = (userId) => {
    console.log(`Add friend: ${userId}`);
    // Implement the logic to add a friend
  };

  const onRemoveFriend = (userId) => {
    console.log(`Remove friend: ${userId}`);
    // Implement the logic to remove a friend
  };

  return (
    <div className="search-results">
      {users
        .filter((user) => user.user_id !== globalVar.username) // Filter out the current user
        .map((user, index) => (
          <div key={index} className="profile-card">
            <div className="profile-image-container">
              <img
                src={user.profile_pic || "default-profile.png"} // Replace with the path to your default image
                alt={user.user_id}
                className="profile-image"
              />
            </div>
            <div className="profile-name">{user.user_id}</div>
            {globalVar.username !== user.user_id && // Check if it's not the current user
              (checkIsFriend(user.user_id) ? (
                <button onClick={() => onRemoveFriend(user.user_id)}>
                  Remove
                </button>
              ) : (
                <button onClick={() => onAddFriend(user.user_id)}>Add</button>
              ))}
          </div>
        ))}
    </div>
  );
};

export default UserList;
