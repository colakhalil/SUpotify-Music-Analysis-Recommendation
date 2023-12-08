import React from "react";

// Example component that takes in 'users' and 'friendsData' as props
const UserList = ({ users, friendsData }) => {
  const checkIsFriend = (userId) => {
    return friendsData.some((friend) => friend.name === userId);
  };

  const onAddFriend = (userId) => {
    console.log(`Add friend: ${userId}`);
  };

  const onRemoveFriend = (userId) => {
    console.log(`Remove friend: ${userId}`);
  };

  return (
    <div className="search-results">
      {users.map((user, index) => (
        <div key={index} className="profile-card">
          <div className="profile-image-container">
            <img
              src={user.profile_pic || "default-profile.png"} // Replace with the path to your default image
              alt={user.user_id}
              className="profile-image"
            />
          </div>
          <div className="profile-name">{user.user_id}</div>
          {checkIsFriend(user.user_id) ? (
            <button onClick={() => onRemoveFriend(user.user_id)}>Remove</button>
          ) : (
            <button onClick={() => onAddFriend(user.user_id)}>Add</button>
          )}
        </div>
      ))}
    </div>
  );
};

export default UserList;
