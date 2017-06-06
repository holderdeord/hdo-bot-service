import React from 'react';
import PropTypes from 'prop-types';
import { ManuscriptTypeEnum } from "../utils/enums";
import ManuscriptItemForm from "./ManuscriptItemForm";

const ManuscriptForm = ({
                          manuscript,
                          addManuscriptItem,
                          changeManuscriptItemProperty,
                          changeManuscriptProperty,
                          deleteManuscriptItem,
                          onSubmit
                        }) => {
  return (
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
          <div className="well">
            {manuscript.items.map(item => (
              <ManuscriptItemForm key={item.order}
                                  item={item}
                                  manuscript={manuscript}
                                  changeManuscriptItemProperty={changeManuscriptItemProperty}
                                  deleteManuscriptItem={deleteManuscriptItem}/>
            ))}
            <button className="btn btn-link" type="button"
                    onClick={() => addManuscriptItem()}>
              Add item
            </button>
          </div>
          <button type="submit" className="btn btn-default">Submit</button>
        </form>
      </div>
      <div className="col-md-6">Preview</div>
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
  onSubmit: PropTypes.func.isRequired
};

export default ManuscriptForm;
