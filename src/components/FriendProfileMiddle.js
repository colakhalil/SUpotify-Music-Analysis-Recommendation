import React, { useState, useEffect } from 'react';
import axios from 'axios';
import UserPart from './subcomponents/UserPart';
import MonthlyAverageRatingsChart from "./subcomponents/FriendMonthlyR";
import SongsAddedByPerformerChart from "./subcomponents/FriendSongsAddedChart";

import globalVar from '../global';

const FriendProfileMiddle = ({ friendEmail }) => {
  const [friendData, setFriendData] = useState(null);
  const [isFriend, setIsFriend] = useState(false);

  useEffect(() => {
    // Replace 'x' with the actual endpoint
    const apiEndpoint = `http://127.0.0.1:8008/friend_data/${friendEmail}`;

    axios.get(apiEndpoint)
      .then((response) => {
        setFriendData(response.data);
        setIsFriend(response.data.isFriend);
        console.log('Fetched friend data:', response.data);
      })
      .catch((error) => {
        console.error('API request error:', error);
      });
  }, [friendEmail]);

  const handleFriendshipToggle = () => {
    const apiEndpoint = `http://127.0.0.1:8008/toggle_friend/${friendEmail}`;
    // Implement the API call to add or remove a friend
    axios.post(apiEndpoint, { isFriend: !isFriend })
      .then((response) => {
        setIsFriend(!isFriend);
        console.log(response.data.message); // Expected message: "Friend added" or "Friend removed"
      })
      .catch((error) => {
        console.error('Error toggling friend status:', error);
      });
  };

  return (

    <div className="main-container">
      <div className="content-container">
        <UserPart userData={friendData} />
        <div className="friendship-button-container">
          <button onClick={handleFriendshipToggle} className="friend-toggle-btn">
            {isFriend ? 'Remove Friend' : 'Add Friend'}
          </button>
        </div>
        <div style={{ display: "flex" }}>
            <MonthlyAverageRatingsChart />
            <SongsAddedByPerformerChart />
        </div>
      </div>
    </div>
  );
};

export default FriendProfileMiddle;
