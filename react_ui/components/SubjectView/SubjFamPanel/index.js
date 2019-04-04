import React from 'react';
import PropTypes from 'prop-types';
import * as SubjFamActions from '../../../actions/subjFam';
import * as SubjectActions from '../../../actions/subject';
import SubjFamCardView from './SubjFamCardView';
import { connect } from 'react-redux';

class SubjFamPanel extends React.Component {
  componentDidMount() {
    const { dispatch } = this.props;
    dispatch(SubjFamActions.fetchSubjFam(
      this.props.activeProtocolId,
      this.props.activeSubject.id));
    dispatch(SubjectActions.fetchSubjects(this.props.activeProtocolId));
    dispatch(SubjFamActions.fetchRelationshipTypes());
  }

  componentWillUnmount() {
    const { dispatch } = this.props;
    dispatch(SubjFamActions.clearSubjFamState());
  }


    render() {
      return (<SubjFamCardView />);
    }
}
SubjFamPanel.propTypes = {
  dispatch: PropTypes.func,
  protocol: PropTypes.object,
  activeSubject: PropTypes.object,
  activeRecord: PropTypes.object,
  activeProtocolId: PropTypes.number,
  subjFam: PropTypes.object,
  isFetching: PropTypes.bool,
  subjects: PropTypes.array,
  relTypes: PropTypes.array,
};

function mapStateToProps(state) {
  return {
    subjFam: {
      isFetching: state.subjFam.isFetching,
      items: state.subjFam,
      relType: state.subjFam.relType,
    },
    activeSubject: state.subject.activeSubject,
    activeRecord: state.record.activeRecord,
    activeProtocol: state.protocol.activeProtocol,
    activeProtocolId: state.protocol.activeProtocolId,
    subjects: state.subject.items,
  };
}

export default connect(mapStateToProps)(SubjFamPanel);
