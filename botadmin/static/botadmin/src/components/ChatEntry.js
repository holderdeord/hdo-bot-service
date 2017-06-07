import React from 'react';
import './ChatEntry.css';

const ChatEntry = ({ isBot, hasContainer, children }) => {
  console.log(hasContainer);
  return (
    <div className="media">
      {isBot ? (
        <div className="media-left media-bottom">
          <img className="user-avatar" src="/img/bot_picture.png" alt="Bot picture"/>
        </div>
      ) : null}
      <div className="media-body">
      {hasContainer ? (
        <ul className="list-group">{children}</ul>
      ) : children}
      </div>
      {!isBot ? (
        <div className="media-right media-bottom">
          <img className="user-avatar" src="/img/fallback_avatar.png" alt="User picture"/>
        </div>
      ) : null}
    </div>
  );
};

export default ChatEntry;
