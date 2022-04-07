import React from "react";
import { DiGithubBadge } from "react-icons/di";

export const Header = () => {
  return (
    <div className="header">
      <h className="title">Rivals Replay Stats</h>
      <a className="logo" href="https://github.com/SimonK5/replay-rollback">
        <DiGithubBadge size={40} className="logo" />
      </a>
    </div>
  );
};
