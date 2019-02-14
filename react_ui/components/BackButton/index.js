import React from 'react';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';

class BackButton extends React.Component {
  constructor(props) {
    super(props);
    this.handleClick = this.handleClick.bind(this);
  }

  handleClick() {
    this.context.history.goBack();
  }

  render() {
    const divStyle = {
      backgroundColor: 'white',
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
      fontSize: '2em',
      color: '#7AC29A',
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

BackButton.contextTypes = {
  history: PropTypes.object,
};

export default connect()(BackButton);
