import React from 'react';
import PropTypes from 'prop-types';
import { ManuscriptTypeEnum } from "../utils/enums";
import { Link } from "react-router-dom";
import ManuscriptPreview from "./ManuscriptPreview";
import './ManuscriptForm.css';
import { Navbar, Tab, Tabs, Well } from "react-bootstrap";
import ManuscriptItemForm from "./ManuscriptItemForm";
import * as queryString from 'query-string';
import ManuscriptAlternativeForm from "./ManuscriptAlternativeForm";

const ManuscriptForm = ({
                          hdo_categories,
                          manuscript,
                          manuscripts,
                          addManuscriptItem,
                          changeManuscriptAlternativeProperty,
                          changeManuscriptItemProperty,
                          changeManuscriptProperty,
                          deleteManuscriptItem,
                          moveManuscriptItemDown,
                          moveManuscriptItemUp,
                          onSubmit,
                          onTabSelect,
                          location
                        }) => {
  const parsed = queryString.parse(location.search);
  const defaultActiveTab = parsed.tab ? parseInt(parsed.tab, 10) : 1;
  return (
    <form className="manuscript-form" onSubmit={event => onSubmit(event, manuscript)}>
      <ol className="breadcrumb">
        <li>
          <Link to="/">Admin</Link>
        </li>
        <li className="active">{manuscript.name}</li>
      </ol>
      <div className="row">
        <div className="col-md-6">
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
          <Tabs id="ManuscriptTypeOptions" onSelect={onTabSelect} defaultActiveKey={defaultActiveTab}>
            <Tab eventKey={1} title="Items">
              <Well>
                {manuscript.items.map((item, index) => (
                  <ManuscriptItemForm key={item.order}
                                      item={item}
                                      manuscript={manuscript}
                                      manuscripts={manuscripts}
                                      changeManuscriptItemProperty={changeManuscriptItemProperty}
                                      deleteManuscriptItem={deleteManuscriptItem}
                                      moveManuscriptItemDown={moveManuscriptItemDown}
                                      moveManuscriptItemUp={moveManuscriptItemUp}/>
                ))}
                <button className="btn btn-default" type="button"
                        onClick={() => addManuscriptItem()}>
                  Add item
                </button>
              </Well>
            </Tab>
            <Tab eventKey={2} title="Voter guide" disabled={manuscript.type !== ManuscriptTypeEnum.ElectoralGuide.key}>
              <div className="form-group">
                <label>HDO kategori</label>
                <select className="form-control"
                        onSelect={(event) => changeManuscriptProperty(event, 'hdo_category')}
                        defaultValue={manuscript.hdo_category}>
                  {hdo_categories.map(category => (
                    <option key={`hdo-category-${category.pk}`} value={category.pk}>{category.name}</option>
                  ))}
                </select>
              </div>
              <div className="checkbox">
                <label>
                  <input type="checkbox"
                         name="is_first_in_category"
                         onChange={(event) => changeManuscriptProperty(event, 'is_first_in_category')}
                         checked={manuscript.is_first_in_category}/>
                  &nbsp;
                  Er først i kategorien
                </label>
              </div>
              <div className="form-group">
                <label>Partier involert ({manuscript.voter_guide_parties.length})</label>
                <p>{manuscript.voter_guide_parties.join(', ')}</p>
              </div>
              <Well>
                {manuscript.voter_guide_alternatives.map((alternative, index) => (
                  <ManuscriptAlternativeForm alternative={alternative}
                                             changeManuscriptAlternativeProperty={changeManuscriptAlternativeProperty}
                                             key={`voter-guide-alternative-${alternative.pk}`}
                                             index={index}/>
                ))}
              </Well>
            </Tab>
            <Tab eventKey={3} title="Quiz" disabled={manuscript.type !== ManuscriptTypeEnum.Quiz.key}>
              <p>Admin for quiz</p>
            </Tab>
          </Tabs>
        </div>
        <div className="col-md-6">
          <label>Preview</label>
          <div className="well">
            <ManuscriptPreview manuscript={manuscript} manuscripts={manuscripts}/>
          </div>
        </div>
      </div>
      <Navbar fixedBottom={true}>
        <Navbar.Form>
          <button type="submit" className="btn btn-primary btn-block">Submit</button>
        </Navbar.Form>
      </Navbar>
    </form>
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
  changeManuscriptAlternativeProperty: PropTypes.func.isRequired,
  changeManuscriptItemProperty: PropTypes.func.isRequired,
  changeManuscriptProperty: PropTypes.func.isRequired,
  deleteManuscriptItem: PropTypes.func.isRequired,
  moveManuscriptItemDown: PropTypes.func.isRequired,
  moveManuscriptItemUp: PropTypes.func.isRequired,
  onSubmit: PropTypes.func.isRequired
};

export default ManuscriptForm;
