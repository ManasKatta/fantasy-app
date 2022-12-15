import React from "react";
// import { useState } from "react";
// import axios from "axios";
import Players from "../Players.json";

const PlayerCard = ({ playerID }) => {
    const url = `https://www.nfl.com/players/${Players[playerID].first_name}-${Players[playerID].last_name}/`;
    const teamURL = `https://sleepercdn.com/images/team_logos/nfl/${Players[playerID].team.toLowerCase()}.png`
  const pfpURL = `https://sleepercdn.com/content/nfl/players/${playerID}.jpg`;
  return (
    <div className="py-0.5">
        <a href={url}>
      <div className="container mx-auto">
        <div className="flex bg-[#1e1e1e] border border-[#121212] rounded-xl overflow-hidden items-center justify-start hover:bg-[#ffb7c5]">
          <div className="relative w-32 h-20 flex-shrink-0">
            <div className="absolute left-0 top-0 w-full h-full flex items-center justify-center">
              <img
                alt={Players[playerID].first_name}
                className="absolute left-0 top-0 w-full h-full object-cover object-center transition duration-50"
                loading="loading..."
                src={pfpURL}
              />
            </div>
          </div>

          <div className="p-3">
            <p className="text-sm line-clamp-1">
              {Players[playerID].full_name}
            </p>

            <p className="text-sm text-[#a2d4ef] mt-1 line-clamp-2">
              {Players[playerID].position} <img className="h-7 w-7 inline" src = {teamURL}/>
              <br />
              {Players[playerID].college}
            </p>
          </div>
        </div>
      </div>
      </a>
    </div>
  );
};

export default PlayerCard;
