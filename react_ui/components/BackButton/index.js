import React from 'react';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';
import { withRouter } from 'react-router';
import styles from './BackButton.css';

class BackButton extends React.Component {
  constructor(props) {
    super(props);
    this.handleClick = this.handleClick.bind(this);
  }

  handleClick() {
    this.props.history.goBack();
  }

  render() {
  
    return (
      <div onClick={this.handleClick} className={styles.divStyle}>
        <i className={styles.tiArrowLeft}></i>
      </div>
    );
  }
}

BackButton.propTypes = {
  history: PropTypes.object,
};

export default withRouter(connect()(BackButton));
