import React, { useState }  from "react";
import FriendItem from "./subcomponents/FriendItem";
import globalVar from "../global.js"; // Assuming globalVar holds your user info

const FriendActivity = ({
  friendsData,
  setCurrentPlace,
  setFriendsUpdate,
  friendsUpdate,
  viewFriendProfile
}) => {
  const changeFriendship = async (friend_id, index) => {
    let rateSharing = "private";

    // Assuming you want to check the lastListenedSong of the specific friend at index
    if (
      friendsData[index] &&
      friendsData[index].lastListenedSong === "private"
    ) {
      rateSharing = "public";
    } else {
      rateSharing = "private";
    }

    console.log("Friends data: ", friendsData);
    let userId = globalVar.username; // Assuming this is how you get the logged-in user's ID

    console.log("Rate Sharing:", rateSharing);
    console.log("UserID:", userId);
    console.log("FriendID:", friend_id);
    try {
      const response = await fetch(
        `http://127.0.0.1:8008/update_friendship/${userId}`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            // Add any other headers your API might require
          },
          body: JSON.stringify({
            friend_id: friend_id,
            rate_sharing: rateSharing,
          }),
        }
      );

      const data = await response.json();
      if (response.ok) {
        console.log("Friendship Updated:", data); // Success response
      } else {
        console.error("Error Updating Friendship:", data); // Handle error response
      }
    } catch (error) {
      console.error("Error:", error);
    }
    setFriendsUpdate(!friendsUpdate);
    console.log("friendsUpdate:", friendsUpdate);
  };

  const [currentViewedFriendName, setCurrentViewedFriendName] = useState('');

  const handleFriendSelection = (friendName) => {
    setCurrentViewedFriendName(friendName); // Set the currently viewed friend's name
    setCurrentPlace("friend"); // Switch to the "friend" view
  };

  return (
    <div className="friend-bar" style={{ overflow: "auto" }}>
      {friendsData.map((friend, index) => (
        <React.Fragment key={friend.name}>
          <FriendItem
            friend={friend}
            setCurrentPlace={setCurrentPlace}
            onSelectFriend={viewFriendProfile}
          />
          <button onClick={() => changeFriendship(friend.name, index)}>
            Change Friendship Type
          </button>
        </React.Fragment>
      ))}
    </div>
  );
};

export default FriendActivity;
