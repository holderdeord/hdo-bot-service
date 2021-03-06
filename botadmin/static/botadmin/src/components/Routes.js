import React from 'react';

import {
  BrowserRouter,
  Route,
  Switch,
} from 'react-router-dom'

import Admin from "../containers/Admin";
import NoMatch from "./NoMatch";
import EditManuscript from "../containers/EditManuscript";
import CreateManuscript from "../containers/CreateManuscript";
import Header from "./Header";

const Routes = () => (
  <BrowserRouter basename='/botadmin'>
    <div>
      <Header />
      <div className="container">
        <Switch>
          <Route exact path="/" component={Admin}/>
          <Route exact path="/create" component={CreateManuscript}/>
          <Route exact path="/create/:tabId" component={CreateManuscript}/>
          <Route exact path="/create/:tabId/:alternativeIndex" component={CreateManuscript}/>
          <Route exact path="/edit/:manuscriptId" component={EditManuscript}/>
          <Route exact path="/edit/:manuscriptId/:tabId" component={EditManuscript}/>
          <Route exact path="/edit/:manuscriptId/:tabId/:alternativeIndex" component={EditManuscript}/>
          <Route component={NoMatch}/>
        </Switch>
      </div>
    </div>
  </BrowserRouter>
);

export default Routes;
