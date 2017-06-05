import React, { Component } from 'react';

import {
  BrowserRouter as Router,
  Link,
  Route,
  Switch
} from 'react-router-dom'

import AdminComponent from "./AdminComponent";
import ManuscriptViewComponent from "./ManuscriptViewComponent";
import NoMatch from "./NoMatch";
import ManuscriptCreateComponent from "./ManuscriptCreateComponent";

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
            <Route exact path="/create" component={ManuscriptCreateComponent}/>
            <Route exact path="/view/:manuscriptId" component={ManuscriptViewComponent}/>
            <Route component={NoMatch}/>
          </Switch>
        </div>
      </Router>
    )
  }
}

export default Routes;
