import React, { Component } from 'react';

import {
  BrowserRouter as Router, Link,
  Route,
  Switch
} from 'react-router-dom'

import Admin from "../containers/Admin";
import NoMatch from "./NoMatch";
import NavItem from "./NavItem";
import EditManuscript from "../containers/EditManuscript";
import CreateManuscript from "../containers/CreateManuscript";

const Routes = () => (
  <Router>
    <div>
      <header>
        <nav className="navbar navbar-default">
          <div className="container">
            <Link className="navbar-brand" to="/">Holder de ord</Link>
            <ul className="nav navbar-nav">
              <NavItem activeClassName="active" to="/">Admin</NavItem>
            </ul>
          </div>
        </nav>
      </header>
      <div className="container">
        <Switch>
          <Route exact path="/" component={Admin}/>
          <Route exact path="/create" component={CreateManuscript}/>
          <Route exact path="/edit/:manuscriptId" component={EditManuscript}/>
          <Route component={NoMatch}/>
        </Switch>
      </div>
    </div>
  </Router>
);

export default Routes;
