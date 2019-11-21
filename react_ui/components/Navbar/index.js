import { connect } from 'react-redux';
import React from 'react';
import ProjectMenu from '../ProjectMenu'
import PropTypes from 'prop-types';
import { Link } from "react-router-dom";
import { HashRouter } from 'react-router-dom';


class Navbar extends React.Component {
  render() {
    const protocol = this.props.activeProtocolId;
    let subjectSelectUrl = null;
    let inDs = false;

    if (protocol) {
      subjectSelectUrl = `/dataentry/protocol/${protocol}`;
    } else {
      inDs = true;
    }
     if (!inDs) {
      return (
        <HashRouter>
        <div
          className="navbar navbar-ct-primary navbar-fixed-top"
          role="navigation" >
          <div className="navbar-header">
            <div className="navbar-brand">
              <Link to="/"  className="navbar-text">Biorepository Portal</Link>
            </div>
          </div>

          <div className="collapse navbar-collapse navbar-ex1-collapse">
            <ul className="nav navbar-nav navbar-right pull-right">
              <li><Link to={subjectSelectUrl} className="navbar-text">Subjects</Link></li>
              <li><Link to="/" className="navbar-text">Projects</Link></li>
              <li><a href="/logout" className="navbar-text" >Logout</a></li>
            </ul>
          </div>
        </div>
        </HashRouter>
      );
    }
    return null;
  }
}

Navbar.propTypes = {
  activeProtocolId: PropTypes.number,
};

function mapStateToProps(state) {
  return {
    activeProtocolId: state.protocol.activeProtocolId,
  };
}

export default connect(mapStateToProps)(Navbar);
