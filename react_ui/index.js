// import 'babel-polyfill';
import React from 'react';
import App from './containers/App';
import Navbar from './components/Navbar';
import ProjectMenu from './components/ProjectMenu';
import SubjectSelect from './components/SubjectSelect';
import SubjectView from './components/SubjectView';
import { Provider } from 'react-redux';
import { Router, Route, IndexRoute, browserHistory } from 'react-router';
import { render } from 'react-dom';
import store from './store';



class ProjectList extends React.Component {
/* eslint-disable no-underscore-dangle*/
// Very manually constraining this to the root path until we establish proper
// routing and views. This allows us to bounce out of the single page app paradigm
// and into existing ehb-datasource url paths
  if ( window.location.pathname === '/' ) {
    render(
      <Provider store={store}>
        <Router history={browserHistory}>
          <Route path="/" component={App}>
            <IndexRoute component={ProjectMenu} />
            <Route path="dataentry/protocol/:id" component={SubjectSelect} />
            <Route
              path="dataentry/protocol/:prot_id/subject/:sub_id(/:edit)"
              component={SubjectView}
            />
          </Route>
        </Router>
      </Provider>,
      document.getElementById('react')
    );
  } else {
    render(
      <Provider store={store}>
        <Navbar />
      </Provider>,
      document.getElementById('react'));
  }
}
export default ProjectList;
