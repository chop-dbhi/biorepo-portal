import React from 'react';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';
import { withRouter } from 'react-router';

class BackButton extends React.Component {
  constructor(props) {
    super(props);
    this.handleClick = this.handleClick.bind(this);
  }

  handleClick() {
    this.props.history.goBack();
  }

  render() {
    const divStyle = {
      backgroundColor: '#e7f2f5',
      opacity: '0.7',
      width: '75px',
      position: 'fixed',
      zIndex: 99,
      left: '90px',
      bottom: '10px',
      height: '75px',
      textAlign: 'center',
      borderRadius: '50%',
      boxShadow: '5px 5px 5px rgba(204, 197, 185, 0.7)',
      cursor: 'pointer',
    };
    const arrowStyle = {
      marginTop: '10px',
      fontSize: '3em',
      color: '#34BFED', 
      position: 'relative',
      top: '20px',
    };
    return (
      <div onClick={this.handleClick} style={divStyle}>
        <i style={arrowStyle} className="ti-arrow-left"></i>
      </div>
    );
  }
}

BackButton.propTypes = {
  history: PropTypes.object,
};

export default withRouter(connect()(BackButton));
