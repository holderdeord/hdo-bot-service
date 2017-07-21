import React from 'react';
import { ManuscriptTypeEnum } from "../utils/enums";
import { Link } from "react-router-dom";
import ManuscriptPreview from "./ManuscriptPreview";
import './ManuscriptForm.css';
import { Button, Navbar, Well } from "react-bootstrap";
import ManuscriptFormTabs from "./ManuscriptFormTabs";
import { Sticky, StickyContainer } from 'react-sticky';

const ManuscriptForm = (props) => {
  const {
    changeManuscriptProperty,
    manuscript,
    match,
    onSubmit,
  } = props;
  const defaultActiveTab = match.params.tabId ? parseInt(match.params.tabId, 10) : 1;
  return (
    <form className="manuscript-form" onSubmit={event => onSubmit(event, manuscript)}>
      <ol className="breadcrumb">
        <li>
          <Link to="/">Admin</Link>
        </li>
        <li className="active">{manuscript.name}</li>
      </ol>
      <StickyContainer className="row">
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
          <ManuscriptFormTabs {...props} defaultActiveTab={defaultActiveTab}/>
        </div>
        <div className="col-md-6">
          <Sticky>
            {
              ({
                 style,
                 isSticky,
               }) => {
                const preview_style = {
                  height: isSticky ? document.documentElement.clientHeight - 150 : 'auto'
                };
                return (
                  <div style={style}>
                    <label>Preview</label>
                    <Well>
                      <ManuscriptPreview {...props} style={preview_style}/>
                    </Well>
                  </div>
                )
              }
            }
          </Sticky>
        </div>
      </StickyContainer>
      <Navbar fixedBottom={true}>
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
