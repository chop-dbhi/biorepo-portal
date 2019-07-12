import { connect } from 'react-redux';
import React from 'react';
import ProjectMenu from '../ProjectMenu'
import PropTypes from 'prop-types';
import { Link } from "react-router-dom";
import { HashRouter } from 'react-router-dom';


class Navbar extends React.Component {


  render() {
    const brandStyle = {
      color: '#337ab7',
      marginTop: '0px',
    };

    const navbarStyle = {
      backgroundColor: '#e7f2f5',
      marginBottom: '0 !important',
      border: '0',
      fontFamily: ' "TPRubrik-Regular", sans-serif',
      color: '#337ab7',
    };

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
        <div style={navbarStyle}
        className="navbar navbar-ct-primary navbar-fixed-top"
        role="navigation" >
          <div className="navbar-header">
            <div className="navbar-brand">
              <Link to="/" style={brandStyle} className="navbar-text">Biorepository Portal</Link>
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
