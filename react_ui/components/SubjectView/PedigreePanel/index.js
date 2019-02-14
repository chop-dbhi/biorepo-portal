import React from 'react';
import PropTypes from 'prop-types';
import * as PedigreeActions from '../../../actions/pedigree';
import * as SubjectActions from '../../../actions/subject';
import PedigreeCardView from './PedigreeCardView';
import { connect } from 'react-redux';

// const SubjectPedigreePanel = (props) => {
//   return <SubjectPedigreeCardView />;
// };
//
// SubjectPedigreePanel.propTypes = {
//   edit: React.PropTypes.string,
//   path: React.PropTypes.string,
// };
class PedigreePanel extends React.Component {
  componentDidMount() {
    const { dispatch } = this.props;
    dispatch(PedigreeActions.fetchPedigree(
      this.props.activeProtocolId,
      this.props.activeSubject.id));
    dispatch(SubjectActions.fetchSubjects(this.props.activeProtocolId));
  }

  componentWillUnmount() {
    const { dispatch } = this.props;
    dispatch(PedigreeActions.clearPedigreeState());
  }


    render() {
      return (<PedigreeCardView />);
    }
}
PedigreePanel.propTypes = {
  dispatch: PropTypes.func,
  protocol: PropTypes.object,
  activeSubject: PropTypes.object,
  activeRecord: PropTypes.object,
  activeProtocolId: PropTypes.number,
  pedigree: PropTypes.object,
  isFetching: PropTypes.bool,
  subjects: PropTypes.array,
};

function mapStateToProps(state) {
  return {
    pedigree: {
      isFetching: state.pedigree.isFetching,
      items: state.pedigree,
    },
    activeSubject: state.subject.activeSubject,
    activeRecord: state.record.activeRecord,
    activeProtocol: state.protocol.activeProtocol,
    activeProtocolId: state.protocol.activeProtocolId,
    subjects: state.subject.items,
  };
}

export default connect(mapStateToProps)(PedigreePanel);
// export default PedigreePanel;
// export default connect(SubjectPedigreePanel);
