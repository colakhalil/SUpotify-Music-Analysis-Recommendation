import React from "react";
import FriendItem from "./subcomponents/FriendItem";

const FriendActivity = ({ friendsData }) => {
  return (
    <div className="friend-bar" style={{ overflow: "auto" }}>
      {friendsData.map((friend) => (
        <FriendItem friend={friend} key={friend.name} />
      ))}
    </div>
  );
};

export default FriendActivity;
