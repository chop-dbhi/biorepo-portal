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
    return (
      <div className="back-arrow-div" onClick={this.handleClick}>
        <i className="ti-arrow-left back-arrow"></i>
      </div>
    );
  }
}

BackButton.propTypes = {
  history: PropTypes.object,
};

export default withRouter(connect()(BackButton));
