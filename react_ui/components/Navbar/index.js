import { Link } from 'react-router-dom';
import { connect } from 'react-redux';
import React from 'react';
import PropTypes from 'prop-types';

class Navbar extends React.Component {


  render() {
    const brandStyle = {
      color: '#337ab7',
      marginTop: '0px',
    };
    const navbarStyle = {
      backgroundColor: '#f2efec',
      marginBottom: '0 !important',
      border: '0',
      fontFamily: ' "TPRubrik-Regular", sans-serif',
      color: '#337ab7',
    };
    const protocol = this.props.activeProtocolId;

    let subjectSelectUrl = null;
    let inDs = false;

    if (protocol) {
      subjectSelectUrl = `dataentry/protocol/${protocol}`;
    } else {
      inDs = true;
    }
    if (!inDs) {
      return (
        <div
          style={navbarStyle}
          className="navbar navbar-ct-primary navbar-fixed-top"
          role="navigation"
        >
          <div className="navbar-header">
            <div className="navbar-brand">
              <Link style={brandStyle} className="navbar-text" to={'/'}>
                Biorepository Portal
              </Link>
            </div>
          </div>
          <div className="collapse navbar-collapse navbar-ex1-collapse">
            <ul className="nav navbar-nav navbar-right pull-right">
                {subjectSelectUrl ?
                  <li><Link to={subjectSelectUrl}>Subjects</Link></li> :
                  <div />
                }{
                  protocol ?
                    <li><Link to={'/'}>Projects</Link></li>
                   :
                  null
                }
              <li><a href="/logout">Logout</a></li>
            </ul>
          </div>
        </div>
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
