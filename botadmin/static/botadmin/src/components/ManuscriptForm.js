import React from 'react';
import { ManuscriptTypeEnum } from "../utils/enums";
import { Link } from "react-router-dom";
import ManuscriptPreview from "./ManuscriptPreview";
import './ManuscriptForm.css';
import { Button, Navbar } from "react-bootstrap";
import ManuscriptFormTabs from "./ManuscriptFormTabs";

const ManuscriptForm = (props) => {
  const {
    changeManuscriptProperty,
    manuscript,
    manuscripts,
    onSubmit,
  } = props;
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
                   defaultValue={manuscript.name}
                   onChange={(event) => changeManuscriptProperty(event, 'name')}/>
          </div>
          <div className="form-group">
            <label htmlFor="type">Category</label>
            <select className="form-control" id="type" name="type"
                    defaultValue={manuscript.type}
                    onChange={(event) => changeManuscriptProperty(event, 'type')}>
              {Object.keys(ManuscriptTypeEnum).map(key => (
                <option key={key} value={ManuscriptTypeEnum[ key ].key}>{ManuscriptTypeEnum[ key ].text}</option>
              ))}
            </select>
          </div>
          <ManuscriptFormTabs {...props}/>
        </div>
        <div className="col-md-6">
          <label>Preview</label>
          <div className="well">
            <ManuscriptPreview manuscript={manuscript} manuscripts={manuscripts}/>
          </div>
        </div>
      </div>
      <Navbar fixedBottom={true}>
        {manuscript.has_changes ? (
          <div>test</div>
        ) : null}
        <Navbar.Form>
          <Button type="submit"
                  disabled={!manuscript.has_changes}
                  bsStyle={manuscript.has_changes ? 'primary' : 'default'}
                  block={true}>
            {manuscript.has_changes ? 'Submit changes' : 'No changes done'}
          </Button>
        </Navbar.Form>
      </Navbar>
    </form>
  );
};

export default ManuscriptForm;
