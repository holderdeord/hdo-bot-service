import React from 'react';
import ReactDOM from 'react-dom';
import registerServiceWorker from './registerServiceWorker';
import './index.css';
import Routes from "./components/Routes";
import { adminApp } from "./reducers/index";
import { createStore } from "redux";
import { Provider } from "react-redux";
import 'jquery';
import * as toastr from 'toastr';

toastr.options = {
  closeButton: true
};

const store = createStore(adminApp);

ReactDOM.render(<Provider store={store}>
  <Routes />
</Provider>, document.getElementById('root'));
registerServiceWorker();
