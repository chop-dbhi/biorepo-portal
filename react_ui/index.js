// import 'babel-polyfill';
import React from 'react';
import App from './containers/App';
import Navbar from './components/Navbar';
import ProjectMenu from './components/ProjectMenu';
import SubjectSelect from './components/SubjectSelect';
import SubjectView from './components/SubjectView';

import { Provider } from 'react-redux';
import { Switch, Route} from 'react-router-dom';
import { createStore, applyMiddleware, compose } from 'redux';
import thunk from 'redux-thunk';
import ReactDOM from 'react-dom';
import { createBrowserHistory } from 'history';
import { HashRouter} from 'react-router-dom';
import rootReducer from './reducers/index';
// import { render } from 'react-dom';
// import store from './store';
// var ReactDOM = require('react-dom');


/* eslint-disable no-underscore-dangle */
const composeEnhancers = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;
const store = createStore(
  rootReducer,
  composeEnhancers(
    applyMiddleware(thunk), /* preloadedState, */
  ),
);
/* eslint-enable */

const state = window.__STATE__;
delete window.__STATE__;

// if using exiting html from ehb-datasources then just use navbar react component
if (window.location.pathname.match(/^\/dataentry\/protocoldatasource/ )){
  ReactDOM.hydrate(
    <Provider store={store}>
      <Navbar />
    </Provider>,
    document.getElementById('react'));
} else {
  ReactDOM.hydrate(
    <Provider store={store}>
      <Navbar />
      <HashRouter>
         <Switch>
           <Route path="/dataentry/protocol/:prot_id/subject/:sub_id" component={SubjectView} />
           <Route path="/dataentry/protocol/:id" component={SubjectSelect} />
           <Route exact path="/" component={ProjectMenu}  />
         </Switch>
       </HashRouter>
    </Provider>,
   document.getElementById('react'));
 }
