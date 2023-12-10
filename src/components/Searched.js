import React from "react";
import globalVar from "../global.js";
import "../pagesCSS/SearchBar.css";

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
    <div className="container mt-5">
      <div className="row d-flex justify-content-center">
        <div className="col-md-6">
          <div className="card">
            {/* Assuming this input box is a search or filter for the list */}
            <div className="input-box">
              <input type="text" className="form-control" placeholder="Search..." />
              <i className="fa fa-search"></i>
            </div>
  
            {/* Render user list */}
            {users.filter(user => user.user_id !== globalVar.username)
                  .map((user, index) => (
              <div key={user.user_id} className="list border-bottom">
                <img 
                  src={user.profile_pic || "default-profile.png"} 
                  alt={user.user_id} 
                  className="profile-picture" 
                />
                <div className="d-flex flex-column ml-3">
                  <span>{user.user_id}</span>
                  <small>{/* Additional user info here */}</small>
                </div>
                {globalVar.username !== user.user_id && (
                  checkIsFriend(user.user_id) ? (
                    <button onClick={() => onRemoveFriend(user.user_id)} className="friend-button-remove">
                      Remove
                    </button>
                  ) : (
                    <button onClick={() => onAddFriend(user.user_id)} className="friend-button-add">
                        Add
                    </button>
                  )
                )}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
  
  
  
};

export default UserList;
