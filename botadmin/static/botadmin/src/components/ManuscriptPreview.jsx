import React from 'react';
import { ChatEntryTypeEnum, ManuscriptItemTypeEnum } from "../utils/enums";
import ChatEntry from "./ChatEntry";
import './ManuscriptPreview.css';
import { Button, ButtonToolbar } from "react-bootstrap";
import { Link } from "react-router-dom";

const ManuscriptPreview = ({
                             manuscript,
                             manuscripts,
                             style
                           }) => {
  return (
    <div className="manuscript-preview" style={style}>
      {getChatEntries(manuscript, manuscripts).map(({ isBot, hasContainer, items, itemIndex }, index) => (
        <ChatEntry key={`manuscript-preview-item-${index}`}
                   isBot={isBot}
                   hasContainer={hasContainer}
                   itemIndex={itemIndex}>
          {items.map(({ hasContainer, itemIndex, component }, index) => hasContainer ? (
            <li key={`preview-item-${index}`}
                className="list-group-item">
              {component}
            </li>
          ) : (
            <div key={`preview-item-${index}`}>{component}</div>
          ))}
        </ChatEntry>
      ))}
    </div>
  );
};

export default ManuscriptPreview;

function getChatEntries(manuscript, manuscripts) {
  return manuscript.items
    .reduce((memo, item, index) => [
      ...memo,
      ...getChatEntryFromManuscriptItem(item, manuscript, manuscripts, index)
    ], [])
    .reduce((memo, item) => groupChatEntries(memo, item), [])
    .reverse();
}

function getChatEntryFromManuscriptItem(item, manuscript, manuscripts, itemIndex) {
  const { order, type, text } = item;
  switch (type) {
    case ManuscriptItemTypeEnum.QuickReply.key:
      return [
        {
          type: ChatEntryTypeEnum.Text,
          isBot: true,
          hasContainer: true,
          itemIndex,
          component: text
        },
        {
          type: ChatEntryTypeEnum.Button,
          isBot: false,
          hasContainer: false,
          itemIndex,
          component: (
            <ButtonToolbar className="chat-quick-replies">
              {[ 1, 2, 3 ].map((number) =>
                createReplyButton(
                  item[ `reply_text_${number}` ],
                  item[ `reply_action_${number}` ],
                  order,
                  number
                )
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
          itemIndex,
          component: text
        }
      ];
    case ManuscriptItemTypeEnum.VG_Categories.key:
      const category_manuscripts = manuscripts.filter(manuscript => manuscript.is_first_in_category);
      return [
        {
          type: ChatEntryTypeEnum.Text,
          isBot: true,
          hasContainer: true,
          itemIndex,
          component: (
            <div>
              <p>{text}</p>
              <ol>
                {category_manuscripts.map((manuscript, index) => (
                  <li key={`category-manuscript-text-${index}`}>{manuscript.hdo_category}</li>
                ))}
              </ol>
            </div>
          )
        },
        ...groupCategoryManuscripts(category_manuscripts).map((group, group_index) => {
          return {
            type: ChatEntryTypeEnum.Button,
            isBot: false,
            hasContainer: false,
            itemIndex,
            component: (
              <ButtonToolbar className="chat-quick-replies">
                {group.manuscripts.map((manuscript, index) =>
                  createReplyButton(`#${group_index * 9 + index + 1}`, manuscript.pk, order, manuscript.pk))}
                {group.more ?
                  createReplyButton('Last inn flere', null, order, group_index) :
                  createReplyButton('Last inn de første alternative', null, order, group_index)
                }
              </ButtonToolbar>
            )
          }
        })
      ];
    case ManuscriptItemTypeEnum.VG_Result.key:
      return [
        {
          type: ChatEntryTypeEnum.Text,
          isBot: true,
          hasContainer: true,
          itemIndex,
          component: text
        },
        {
          type: ChatEntryTypeEnum.Text,
          isBot: true,
          hasContainer: true,
          itemIndex,
          component: '[Her vil resultatene vises]'
        }
      ];
    case ManuscriptItemTypeEnum.VG_Questions.key:
      return [
        {
          type: ChatEntryTypeEnum.Text,
          isBot: true,
          hasContainer: true,
          itemIndex,
          component: (
            <div>
              <p>{text}</p>
              <ol>
                {manuscript.voter_guide_alternatives.map((alternative, index) => (
                  <li key={`voter-guide-alternative-text-${index}`}>{alternative.text}</li>
                ))}
              </ol>
            </div>
          )
        },
        {
          type: ChatEntryTypeEnum.Button,
          isBot: false,
          hasContainer: false,
          itemIndex,
          component: (
            <ButtonToolbar className="chat-quick-replies">
              {manuscript.voter_guide_alternatives.map((alternative, index) =>
                createReplyButton(
                  `#${index + 1}`,
                  null,
                  order,
                  alternative.pk
                )
              )}
              {createReplyButton('Ingen er interessante', null, order, -1)}
            </ButtonToolbar>
          )
        }
      ];
    default:
      return [
        {
          type: ChatEntryTypeEnum.Text,
          isBot: true,
          hasContainer: false,
          itemIndex,
          component: `Not supported yet [${type}]`
        }
      ];
  }
}

function groupCategoryManuscripts(category_manuscripts) {
  return category_manuscripts
    .reduce((memo, manuscript, index) => {
      if (index % 9 === 0) {
        memo.unshift({
          more: !!category_manuscripts[ index + 9 ],
          manuscripts: [ manuscript ]
        });
      } else {
        memo[ 0 ].manuscripts.push(manuscript);
      }
      return memo;
    }, [])
    .reverse();
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
