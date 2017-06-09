import React from 'react';
import { ChatEntryTypeEnum, ManuscriptItemTypeEnum } from "../utils/enums";
import ChatEntry from "./ChatEntry";
import './ManuscriptPreview.css';
import { Button, ButtonToolbar } from "react-bootstrap";
import { Link } from "react-router-dom";

const ManuscriptPreview = ({ manuscript }) => (
  <div className="manuscript-preview">
    {getChatEntries(manuscript).map(({ isBot, hasContainer, items }, index) => (
      <ChatEntry key={`manuscript-preview-item-${index}`} isBot={isBot} hasContainer={hasContainer}>
        {items.map(({ hasContainer, component }, index) => hasContainer ? (
          <li key={`preview-item-${index}`} className="list-group-item">{component}</li>
        ) : (
          <div key={`preview-item-${index}`}>{component}</div>
        ))}
      </ChatEntry>
    ))}
  </div>
);

export default ManuscriptPreview;

function getChatEntries(manuscript) {
  return manuscript.items
    .reduce((memo, item) => [ ...memo, ...getChatEntryFromManuscriptItem(item) ], [])
    .reduce((memo, item) => groupChatEntries(memo, item), [])
    .reverse();
}

function getChatEntryFromManuscriptItem(item) {
  const { order, type, text } = item;
  switch (type) {
    case ManuscriptItemTypeEnum.QuickReply.key:
      return [
        {
          type: ChatEntryTypeEnum.Text,
          isBot: true,
          hasContainer: true,
          component: text
        },
        {
          type: ChatEntryTypeEnum.Button,
          isBot: false,
          hasContainer: false,
          component: (
            <ButtonToolbar className="chat-quick-replies">
              {[ 1, 2, 3 ].map((number) => createReplyButton(item[ `reply_text_${number}` ],
                item[ `reply_action_${number}` ],
                order,
                number)
              )}
            </ButtonToolbar>
          )
        }
      ];
    case ManuscriptItemTypeEnum.Text.key:
      return [
        {
          type: ChatEntryTypeEnum.Text,
          isBot: true,
          hasContainer: true,
          component: text
        }
      ];
    default:
      return [
        {
          type: ChatEntryTypeEnum.Text,
          isBot: true,
          hasContainer: false,
          component: `Not supported yet [${type}]`
        }
      ];
  }
}

function groupChatEntries(memo, item) {
  if (memo.length === 0 || memo[ 0 ].isBot !== item.isBot) {
    memo.unshift({
      isBot: item.isBot,
      hasContainer: item.hasContainer,
      items: []
    });
  }
  memo[ 0 ].items.push(item);
  return memo;
}

function createReplyButton(replyText, replyAction, order, number) {
  const key = `chat-quick-reply-button-${order}-${number}`;
  switch (true) {
    case !!replyText && !!replyAction:
      return (
        <Link key={key} className="btn btn-default" to={`/edit/${replyAction}`}>{replyText}</Link>
      );
    case !!replyText:
      return (
        <Button key={key}>{replyText}</Button>
      );
    default:
      return [];
  }
}
