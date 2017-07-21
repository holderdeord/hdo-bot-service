import React from 'react';
import ManuscriptItemForm from "./ManuscriptItemForm";
import { ManuscriptTypeEnum } from "../utils/enums";
import { Button, Tab, Tabs, Well } from "react-bootstrap";
import ManuscriptAlternativeForm from "./ManuscriptAlternativeForm";
import PromisesModal from "./PromisesModal";

const ManuscriptFormTabs = (props) => {
  const {
    addManuscriptAlternative,
    addManuscriptItem,
    changeManuscriptProperty,
    defaultActiveTab,
    hdo_categories,
    manuscript,
    onTabSelect,
  } = props;
  return (
    <Tabs id="ManuscriptTypeOptions" onSelect={onTabSelect} defaultActiveKey={defaultActiveTab}>
      <Tab eventKey={1} title="Items">
        <Well>
          {manuscript.items.map((item, index) => (
            <ManuscriptItemForm key={item.order}
                                item={item}
                                index={index}
                                {...props}/>
          ))}
          <Button bsSize="small"
                  onClick={() => addManuscriptItem()}>
            Add item
          </Button>
        </Well>
      </Tab>
      <Tab eventKey={2} title="Voter guide" disabled={manuscript.type !== ManuscriptTypeEnum.ElectoralGuide.key}>
        <div className="form-group">
          <label>HDO category</label>
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
            {' '}
            First in category
          </label>
        </div>
        <div className="form-group">
          <label>Parties involved ({manuscript.voter_guide_parties.length})</label>
          <p>{manuscript.voter_guide_parties.join(', ')}</p>
        </div>
        <Well>
          {manuscript.voter_guide_alternatives.map((alternative, index) => (
            <ManuscriptAlternativeForm alternative={alternative}
                                       key={`voter-guide-alternative-${alternative.pk}`}
                                       index={index}
                                       {...props}/>
          ))}
          <Button bsSize="small"
                  onClick={() => addManuscriptAlternative()}>
            Add alternative
          </Button>
        </Well>
        <PromisesModal {...props}/>
      </Tab>
      <Tab eventKey={3} title="Quiz" disabled={manuscript.type !== ManuscriptTypeEnum.Quiz.key}>
        <p>Admin for quiz</p>
      </Tab>
    </Tabs>
  );
};

export default ManuscriptFormTabs;
