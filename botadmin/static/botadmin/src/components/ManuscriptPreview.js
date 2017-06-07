import React from 'react';
import { ManuscriptItemTypeEnum } from "../utils/enums";
import ChatEntry from "./ChatEntry";
import './ManuscriptPreview.css';

const ManuscriptPreview = ({ manuscript }) => (
  <div className="manuscript-preview">
    {groupManuscriptIntoEntries(manuscript).map(({ isBot, hasContainer, items }, index) => (
      <ChatEntry key={`manuscript-preview-item-${index}`} isBot={isBot} hasContainer={hasContainer}>
        {items.map(({ order, text, type }) => hasContainer ? (
          <li key={`preview-item-${order}`} className="list-group-item">{generateItemMarkup({ order, text, type })}</li>
        ) : (
          <div key={`preview-item-${order}`}>{generateItemMarkup({ order, text, type })}</div>
        ))}
      </ChatEntry>
    ))}
  </div>
);

export default ManuscriptPreview;

function generateItemMarkup({ order, text, type }) {
  switch (type) {
    case ManuscriptItemTypeEnum.Text.key:
      return text;
    case ManuscriptItemTypeEnum.Button.key:
      return (
        <div className="text-right">
          <button type="button" className="btn btn-default">{text}</button>
        </div>
      );
  }
  return (
    <div key={`preview-item-${order}`}>Not supported yet</div>
  );
}

function groupManuscriptIntoEntries(manuscript) {
  return manuscript.items
    .map(item => {
      return {
        ...item,
        isBot: isItemBotEntry(item.type),
        hasContainer: hasContainerEntry(item.type)
      };
    })
    .reduce((memo, item) => {
      if (memo.length === 0 || memo[ 0 ].isBot !== item.isBot) {
        memo.unshift({
          isBot: item.isBot,
          hasContainer: item.hasContainer,
          items: []
        });
      }
      memo[ 0 ].items.push(item);
      return memo;
    }, [])
    .reverse();
}

function hasContainerEntry(type) {
  return type === ManuscriptItemTypeEnum.Text.key;
}

function isItemBotEntry(type) {
  return type === ManuscriptItemTypeEnum.Text.key;
}