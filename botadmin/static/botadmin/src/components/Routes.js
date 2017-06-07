import React from 'react';

import {
  BrowserRouter as Router,
  Route,
  Switch
} from 'react-router-dom'

import Admin from "../containers/Admin";
import NoMatch from "./NoMatch";
import EditManuscript from "../containers/EditManuscript";
import CreateManuscript from "../containers/CreateManuscript";
import Header from "./Header";

const Routes = () => (
  <Router>
    <div>
      <Header />
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
