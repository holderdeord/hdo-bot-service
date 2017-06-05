import React, { Component } from 'react';

import {
  BrowserRouter as Router,
  Link,
  Route,
  Switch
} from 'react-router-dom'

import AdminComponent from "./AdminComponent";
import ManuscriptForm from "./ManuscriptForm";
import ManuscriptViewComponent from "./ManuscriptViewComponent";
import NoMatch from "./NoMatch";

class Routes extends Component {
  render() {
    return (
      <Router>
        <div>
          <header>
            <Link to="/">Admin</Link>
          </header>
          <Switch>
            <Route exact path="/" component={AdminComponent}/>
            <Route exact path="/create" component={ManuscriptForm}/>
            <Route exact path="/view/:manuscriptId" component={ManuscriptViewComponent}/>
            <Route component={NoMatch}/>
          </Switch>
        </div>
      </Router>
    )
  }
}

export default Routes;
