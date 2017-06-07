import React from 'react';
import { ManuscriptItemTypeEnum, ManuscriptTypeEnum } from "../utils/enums";
import Textarea from 'react-textarea-autosize';

const ManuscriptItemForm = ({
                              item,
                              manuscript,
                              changeManuscriptItemProperty,
                              deleteManuscriptItem,
                              moveManuscriptItemDown,
                              moveManuscriptItemUp
                            }) => {
  const { order, text, type } = item;
  return (
    <div className="panel panel-default">
      <div className="panel-heading">
        Item #{order}
      </div>
      <div className="panel-body">
        <div className="form-group">
          <label htmlFor={`itemType-${order}`}>Type</label>
          <select className="form-control" id={`itemType-${order}`} name="itemType"
                  value={type}
                  onChange={(event) => changeManuscriptItemProperty(event, order, 'type')}>
            {getItemTypes(manuscript.type).map((itemType, index) => (
              <option key={`${manuscript.id}-${order}-${index}`}
                      value={itemType.key}>{itemType.text}</option>
            ))}
          </select>
        </div>
        <div className="form-group">
          <label htmlFor={`itemText-${order}`}>Text</label>
          <Textarea className="form-control" id={`itemText-${order}`} name="itemText"
                    value={text}
                    onChange={(event) => changeManuscriptItemProperty(event, order, 'text')}/>
        </div>
      </div>
      <div className="panel-footer clearfix">
        <div className="btn-toolbar pull-right" role="toolbar">
          <div className="btn-group btn-group-xs" role="group">
            <button type="button" className="btn btn-default"
                    onClick={() => moveManuscriptItemUp(order)}
                    disabled={order === 1}>
              <span className="glyphicon glyphicon-arrow-up"/> Move up
            </button>
            <button type="button" className="btn btn-default"
                    onClick={() => moveManuscriptItemDown(order)}
                    disabled={order === manuscript.items.length}>
              <span className="glyphicon glyphicon-arrow-down"/> Move down
            </button>
          </div>
          <div className="btn-group btn-group-xs" role="group">
            <button type="button" className="btn btn-danger"
                    onClick={() => deleteManuscriptItem(order)}
                    disabled={manuscript.items.length === 1}>
              <span className="glyphicon glyphicon-remove"/> Remove
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ManuscriptItemForm;

function getItemTypes(type) {
  switch (type) {
    case ManuscriptTypeEnum.ElectoralGuide.key:
      return [
        ManuscriptItemTypeEnum.Button,
        ManuscriptItemTypeEnum.Text,
        ManuscriptItemTypeEnum.VG_Categories,
        ManuscriptItemTypeEnum.VG_Questions,
        ManuscriptItemTypeEnum.VG_Result,
      ];
    case ManuscriptTypeEnum.Quiz.key:
      return [
        ManuscriptItemTypeEnum.Button,
        ManuscriptItemTypeEnum.Text,
        ManuscriptItemTypeEnum.Quiz_Result,
        ManuscriptItemTypeEnum.Quiz_PromisesChecked,
        ManuscriptItemTypeEnum.Quiz_PartySelect,
        ManuscriptItemTypeEnum.Quiz_PartyBool,
      ];
  }
  return [
    ManuscriptItemTypeEnum.Button,
    ManuscriptItemTypeEnum.Text,
  ];
}
