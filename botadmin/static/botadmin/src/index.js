import React from 'react';
import ReactDOM from 'react-dom';
import registerServiceWorker from './registerServiceWorker';
import './index.css';
import Routes from "./components/Routes";
import { adminApp } from "./reducers/index";
import { createStore } from "redux";
import { Provider } from "react-redux";

// importing dependencies to expose
import * as toastr from 'toastr';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap/dist/css/bootstrap-theme.css';
import 'toastr/build/toastr.css';

toastr.options = {
  closeButton: true,
  newestOnTop: true
};

const store = createStore(adminApp);

ReactDOM.render(<Provider store={store}>
  <Routes />
</Provider>, document.getElementById('root'));
registerServiceWorker();
