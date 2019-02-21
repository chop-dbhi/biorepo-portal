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
  // static mapDispatchToProps (dispatch) {
  //   return {
  //     fetchProtocols: (null) => dispatch(fetchProtocols(null))
  //   };
  // };
  componentWillMount() {
    console.log("we are at least getting into component Did Mount in project index")
    const { dispatch } = this.props;
    // dispatch(ProtocolActions.setActiveProtocol(null));
    // if (this.props.protocol.items.length === 0 && !this.props.protocol.isFetching) {
    dispatch(ProtocolActions.fetchProtocols());
    }

  render(props) {
    console.log(this.props.protocols)
    // const { fetchProtocols } = props;
    return (
      <div className="card">
        <p>Welcome Back</p>
        <p><i>Select a project for data entry</i></p>
        {this.props.protocols.map((protocol, i) => {
          const url = `dataentry/protocol/${protocol.id}`;
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
}

ProjectMenu.propTypes = {
  dispatch: PropTypes.func,
  protocol: PropTypes.object,
};

const mapStateToProps = state => {
  return {
    protocol: {
      items: state.protocol.items,
      isFetching: state.protocol.isFetching,
    }
  };
};
// const Protocol = connect(mapStateToProps, mapDispatchToProps)(ProjectMenu);
export default connect(mapStateToProps)(ProjectMenu);
// export default Protocol
