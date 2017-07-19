import React from 'react';
import ManuscriptItemForm from "./ManuscriptItemForm";
import { ManuscriptTypeEnum } from "../utils/enums";
import { Tab, Tabs, Well } from "react-bootstrap";
import ManuscriptAlternativeForm from "./ManuscriptAlternativeForm";
import PromisesModal from "./PromisesModal";
import { withRouter } from "react-router-dom";

const ManuscriptFormTabs = withRouter((props) => {
  const {
    addManuscriptItem,
    changeManuscriptProperty,
    closePromisesModal,
    hdo_categories,
    history,
    manuscript,
    match,
    onTabSelect,
    promises_modal,
  } = props;
  const defaultActiveTab = match.params.tabId ? parseInt(match.params.tabId, 10) : 1;
  return (
    <Tabs id="ManuscriptTypeOptions" onSelect={(key) => onTabSelect(key, history)} defaultActiveKey={defaultActiveTab}>
      <Tab eventKey={1} title="Items">
        <Well>
          {manuscript.items.map((item, index) => (
            <ManuscriptItemForm key={item.order}
                                item={item}
                                {...props}/>
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
                                       key={`voter-guide-alternative-${alternative.pk}`}
                                       index={index}
                                       {...props}/>
          ))}
        </Well>
        <PromisesModal promises_modal={promises_modal}
                       closePromisesModal={closePromisesModal}/>
      </Tab>
      <Tab eventKey={3} title="Quiz" disabled={manuscript.type !== ManuscriptTypeEnum.Quiz.key}>
        <p>Admin for quiz</p>
      </Tab>
    </Tabs>
  );
});

export default ManuscriptFormTabs;
