import React, { Component } from 'react';

import {
  BrowserRouter as Router,
  Route,
  Switch
} from 'react-router-dom'

import AdminComponent from "./AdminComponent";
import NoMatch from "./NoMatch";
import ManuscriptCreateComponent from "./CreateManuscriptComponent";
import NavItem from "./NavItem";
import EditManuscriptComponent from "./EditManuscriptComponent";

class Routes extends Component {
  render() {
    return (
      <Router>
        <div>
          <header>
            <nav className="navbar navbar-default">
              <div className="container">
                <span className="navbar-brand">Holder de ord</span>
                <ul className="nav navbar-nav">
                  <NavItem activeClassName="active" to="/">Admin</NavItem>
                </ul>
              </div>
            </nav>
          </header>
          <div className="container">
            <Switch>
              <Route exact path="/" component={AdminComponent}/>
              <Route exact path="/create" component={ManuscriptCreateComponent}/>
              <Route exact path="/view/:manuscriptId" component={EditManuscriptComponent}/>
              <Route component={NoMatch}/>
            </Switch>
          </div>
        </div>
      </Router>
    )
  }
}

export default Routes;
