import React from "react";
import globalVar from "../global.js";

const UserList = ({ users, friendsData, setFriendsUpdate, friendsUpdate }) => {
  const checkIsFriend = (userId) => {
    return friendsData.some((friend) => friend.name === userId);
  };

  const onAddFriend = async (friendUserId) => {
    console.log(`Add friend: ${friendUserId}`);

    const userId = globalVar.username;

    if (!userId) {
      console.error("User ID is undefined or null");
      return; // Exit the function if userId is not defined
    }

    try {
      const response = await fetch(
        `http://127.0.0.1:8008/add_friend/${userId}`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            friend_id: friendUserId,
          }),
        }
      );

      const responseData = await response.json();

      if (responseData.message == "Friend added successfully") {
        console.log("Friend added successfully", responseData);
        setFriendsUpdate(!friendsUpdate);
        // Additional logic after successfully adding a friend
      } else {
        console.error("Error adding friend", responseData);
        // Additional logic in case of an error
      }
    } catch (error) {
      console.error("Network error:", error);
      // Additional logic in case of a network error
    }
  };

  const onRemoveFriend = async (friendUserId) => {
    const userId = globalVar.username;
    // Check if userId is undefined or null
    if (!userId) {
      console.error("User ID is undefined or null");
      return; // Exit the function if userId is not defined
    }

    try {
      const response = await fetch(
        `http://127.0.0.1:8008/remove_friend/${userId}`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            friend_id: friendUserId,
          }),
        }
      );

      const responseData = await response.json();

      if (responseData.message == "Friend removed successfully") {
        console.log("Friend removed successfully", responseData);
        setFriendsUpdate(!friendsUpdate);
        // Additional logic after successfully removing a friend
      } else {
        console.error("Error removing friend", responseData);
        // Additional logic in case of an error
      }
    } catch (error) {
      console.error("Network error:", error);
      // Additional logic in case of a network error
    }
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
