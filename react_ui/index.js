// import 'babel-polyfill';
import React from 'react';
import App from './containers/App';
import Navbar from './components/Navbar';
import ProjectMenu from './components/ProjectMenu';
import SubjectSelect from './components/SubjectSelect';
import SubjectView from './components/SubjectView';
import { Provider } from 'react-redux';
import { Router, Route, BrowserRouter} from 'react-router-dom';
import { createBrowserHistory } from 'history';
import { render } from 'react-dom';
import store from './store';



class ProjectList extends React.Component {
/* eslint-disable no-underscore-dangle*/
// Very manually constraining this to the root path until we establish proper
// routing and views. This allows us to bounce out of the single page app paradigm
// and into existing ehb-datasource url paths

  constructor() {
    const history = createBrowserHistory();
    console.log("ummm ok ")
  }


    render(){
      if ( history.location.pathname === '/' ) {
        console.log("ummm ok ")
        return (
          <Provider store={store}>
            <Router history={browserHistory}>

                <Route path="/" exact component={ProjectMenu} />
                <Route path="dataentry/protocol/:id" component={SubjectSelect} />
                <Route
                  path="dataentry/protocol/:prot_id/subject/:sub_id(/:edit)"
                  component={SubjectView}
                />

            </Router>
          </Provider>,
          document.getElementById('react')
        );
    } else {
      console.log("ummm ok 2")
    return(
      <Provider store={store}>
        <Navbar />
      </Provider>,
      document.getElementById('react'));
    }
  }
}
export default ProjectList;
