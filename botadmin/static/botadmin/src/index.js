import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import registerServiceWorker from './registerServiceWorker';
import './index.css';
import AdminComponent from "./components/AdminComponent";

ReactDOM.render(<AdminComponent />, document.getElementById('root'));
registerServiceWorker();
