import React from 'react';
import { ManuscriptTypeEnum } from "../utils/enums";
import { Link, withRouter } from "react-router-dom";
import ManuscriptPreview from "./ManuscriptPreview";
import './ManuscriptForm.css';
import { Navbar } from "react-bootstrap";
import ManuscriptFormTabs from "./ManuscriptFormTabs";

const ManuscriptForm = withRouter((props) => {
  const {
    changeManuscriptProperty,
    history,
    manuscript,
    manuscripts,
    onSubmit,
  } = props;
  return (
    <form className="manuscript-form" onSubmit={event => onSubmit(event, manuscript, history)}>
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
        <Navbar.Form>
          <button type="submit" className="btn btn-primary btn-block">Submit</button>
        </Navbar.Form>
      </Navbar>
    </form>
  );
});

export default ManuscriptForm;
