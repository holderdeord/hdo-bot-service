import React from 'react';
import PropTypes from 'prop-types';
import { ManuscriptItemTypeEnum, ManuscriptTypeEnum } from "../utils/enums";
import { Link } from "react-router-dom";

const ManuscriptForm = ({
                          manuscript,
                          addManuscriptItem,
                          changeManuscriptItemProperty,
                          changeManuscriptProperty,
                          deleteManuscriptItem,
                          moveManuscriptItemDown,
                          moveManuscriptItemUp,
                          onSubmit
                        }) => {
  return (
    <div>
      <ol className="breadcrumb">
        <li>
          <Link to="/">Admin</Link>
        </li>
        <li className="active">{manuscript.name}</li>
      </ol>
      <div className="row">
        <div className="col-md-6">
          <form onSubmit={event => onSubmit(event, manuscript)}>
            <div className="form-group">
              <label htmlFor="name">Name</label>
              <input className="form-control" type="text" id="name" name="name"
                     value={manuscript.name}
                     onChange={(event) => changeManuscriptProperty(event, 'name')}/>
            </div>
            <div className="form-group">
              <label htmlFor="type">Category</label>
              <select className="form-control" id="type" name="type"
                      value={manuscript.type}
                      onChange={(event) => changeManuscriptProperty(event, 'type')}>
                {Object.keys(ManuscriptTypeEnum).map(key => (
                  <option key={key} value={ManuscriptTypeEnum[ key ].key}>{ManuscriptTypeEnum[ key ].text}</option>
                ))}
              </select>
            </div>
            <label>Items</label>
            <div className="well">
              {manuscript.items.map(({ order, text, type }) => (
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
                      <textarea className="form-control" type="text" id={`itemText-${order}`} name="itemText" rows="1"
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
              ))}
              <button className="btn btn-default" type="button"
                      onClick={() => addManuscriptItem()}>
                Add item
              </button>
            </div>
            <div className="form-group">
              <button type="submit" className="btn btn-primary btn-block">Submit</button>
            </div>
          </form>
        </div>
        <div className="col-md-6">
          <label>Preview</label>
          <div className="well">
            {manuscript.items.map(({ order, text, type }) => {
              switch (type) {
                case ManuscriptItemTypeEnum.Text.key:
                  return (
                    <div key={`preview-item-${order}`}>Text: {text}</div>
                  );
                case ManuscriptItemTypeEnum.Button.key:
                  return (
                    <div key={`preview-item-${order}`}>Button: {text}</div>
                  );
              }
              return (
                <div key={`preview-item-${order}`}>Not supported yet</div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
};

ManuscriptForm.propTypes = {
  manuscript: PropTypes.shape({
    name: PropTypes.string.isRequired,
    type: PropTypes.string.isRequired,
    items: PropTypes.arrayOf(PropTypes.shape({
      order: PropTypes.number.isRequired,
      text: PropTypes.string.isRequired,
      type: PropTypes.string.isRequired
    }))
  }),
  addManuscriptItem: PropTypes.func.isRequired,
  changeManuscriptItemProperty: PropTypes.func.isRequired,
  changeManuscriptProperty: PropTypes.func.isRequired,
  deleteManuscriptItem: PropTypes.func.isRequired,
  moveManuscriptItemDown: PropTypes.func.isRequired,
  moveManuscriptItemUp: PropTypes.func.isRequired,
  onSubmit: PropTypes.func.isRequired
};

export default ManuscriptForm;
