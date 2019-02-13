import React from 'react';
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
  dispatch: React.PropTypes.func,
  protocol: React.PropTypes.object,
  activeSubject: React.PropTypes.object,
  activeRecord: React.PropTypes.object,
  activeProtocolId: React.PropTypes.number,
  pedigree: React.PropTypes.object,
  isFetching: React.PropTypes.bool,
  subjects: React.PropTypes.array,
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
