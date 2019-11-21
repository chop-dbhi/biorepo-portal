import React from 'react';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';
import * as SubjectActions from '../../../actions/subject';

class LinkModeBanner extends React.Component {
  constructor(props) {
    super(props);
    this.dismissLinkMode = this.dismissLinkMode.bind(this);
  }

  dismissLinkMode() {
    const { dispatch } = this.props;
    dispatch(SubjectActions.setLinkMode(false));
  }

  render() {
    return (
      <div className="link-record-banner-style" data-notify="container">
        <span onClick={this.dismissLinkMode} className="link-close">
          <i className="ti-close"></i>
        </span>
        Currently linking records. Please select the second record you would like to link.
      </div>
    );
  }
}

LinkModeBanner.propTypes = {
  dispatch: PropTypes.func,
};

function mapStateToProps(state) {
  return {
    linkMode: state.subject.linkMode,
  };
}

export default connect(mapStateToProps)(LinkModeBanner);
