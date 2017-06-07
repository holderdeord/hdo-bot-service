import React from 'react';
import './ChatEntry.css';
import { Image } from "react-bootstrap";

const ChatEntry = ({ isBot, hasContainer, children }) => {
  return (
    <div className="media">
      {isBot ? (
        <div className="media-left media-bottom">
          <Image className="user-avatar" src="/img/bot_picture.png" alt="Bot" circle/>
        </div>
      ) : null}
      <div className="media-body">
      {hasContainer ? (
        <ul className="list-group">{children}</ul>
      ) : children}
      </div>
      {!isBot ? (
        <div className="media-right media-bottom">
          <Image className="user-avatar" src="/img/fallback_avatar.png" alt="User" circle/>
        </div>
      ) : null}
    </div>
  );
};

export default ChatEntry;
