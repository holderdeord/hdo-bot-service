import React from 'react';
import { ManuscriptItemTypeEnum } from "../utils/enums";
import DeleteManuscriptItemButton from "./DeleteManuscriptItemButton";

const ManuscriptItemForm = ({ item, manuscript, changeManuscriptItemProperty, deleteManuscriptItem }) => {
  const { order, text, type } = item;
  return (
    <div key={order} className="panel panel-default">
      <div className="panel-heading">
        Item #{order}
      </div>
      <div className="panel-body">
        <div className="form-group">
          <label htmlFor={`itemType-${order}`}>Type</label>
          <select className="form-control" id={`itemType-${order}`} name="itemType"
                  value={type}
                  onChange={(event) => changeManuscriptItemProperty(event, order, 'type')}>
            {Object.keys(ManuscriptItemTypeEnum).map(key => (
              <option key={`${manuscript.id}-${order}-${key}`}
                      value={ManuscriptItemTypeEnum[ key ].key}>{ManuscriptItemTypeEnum[ key ].text}</option>
            ))}
          </select>
        </div>
        <div className="form-group">
          <label htmlFor={`itemText-${order}`}>Text</label>
          <input className="form-control" type="text" id={`itemText-${order}`} name="itemText"
                 value={text}
                 onChange={(event) => changeManuscriptItemProperty(event, order, 'text')}/>
        </div>
        <div className="btn-group" role="group">
          <button type="button" className="btn btn-default">
            <span className="glyphicon glyphicon-arrow-up"/> Move up
          </button>
          <button type="button" className="btn btn-default">
            <span className="glyphicon glyphicon-arrow-down"/> Move down
          </button>
          <DeleteManuscriptItemButton manuscript={manuscript}
                                      onClick={() => deleteManuscriptItem(order)}/>
        </div>
      </div>
    </div>
  );
};

export default ManuscriptItemForm;