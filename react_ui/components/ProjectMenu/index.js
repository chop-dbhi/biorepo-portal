import React, { Component } from 'react';
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';
import PropTypes from 'prop-types';
import * as ProtocolActions from '../../actions/protocol';
import { fetchProtocols } from '../../actions/protocol';

class ProjectMenu extends Component {

  constructor(props) {
    super(props);
  }

  componentDidMount() {
    const { dispatch } = this.props;
    dispatch(ProtocolActions.setActiveProtocol(null));
    this.props.dispatch(ProtocolActions.fetchProtocols());
  }

  render(props) {
    if (this.props.protocol.items && this.props.protocol.items.length){
      return (
      <div className="card">
        <p>Welcome Back</p>
        <p><i>Select a project for data entry</i></p>
        {this.props.protocol.items.map((protocol, i) => {
          const url = `/dataentry/protocol/${protocol.id}`;
          return (
            <div key={i} className="lg-col-12">
              <Link
                className="project-row-link"
                to={url}
              >
                {protocol.name}
              </Link>
            </div>
            );
          }, this)}
        </div>
      );
    }
    else {
      return <div>Loading...</div>;
    }
  }
}

ProjectMenu.propTypes = {
  dispatch: PropTypes.func,
  protocol: PropTypes.object,
};

const mapStateToProps = state => ({
    protocol: {
      items: state.protocol.items,
      isFetching: state.protocol.isFetching
  }
});

export default connect(mapStateToProps)(ProjectMenu);
