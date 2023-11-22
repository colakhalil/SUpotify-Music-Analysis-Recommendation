import React from "react";
import FriendItem from "./subcomponents/FriendItem";

const FriendActivity = ({ friendsData, setCurrentPlace }) => {
  return (
    <div className="friend-bar" style={{ overflow: "auto" }}>
      {friendsData.map((friend) => (
        <FriendItem friend={friend} setCurrentPlace = {setCurrentPlace}key={friend.name}/>
      ))}
    </div>
  );
};

export default FriendActivity;
