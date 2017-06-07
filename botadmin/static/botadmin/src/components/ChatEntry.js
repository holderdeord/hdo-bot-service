import React from 'react';
import './ChatEntry.css';

const ChatEntry = ({ isBot, hasContainer, children }) => {
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
    </div>
  );
};

export default ChatEntry;
