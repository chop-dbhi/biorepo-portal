// jscs:disable requireCamelCaseOrUpperCaseIdentifiers
// jscs:disable maximumLineLength
import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { Divider, Header, Image, Segment } from 'semantic-ui-react'
import BackButton from '../BackButton';
import LoadingGif from '../LoadingGif';
import SubjectPanel from './SubjectPanel';
import SubjectCardEdit from './SubjectPanel/SubjectCardEdit'
import RecordPanel from './RecordPanel';
import SubjFamPanel from './SubjFamPanel'
import EditLabelModal from './Modals/EditLabel';
import SubjFamEditView from './SubjFamPanel/subjFamEditView';
import * as ProtocolActions from '../../actions/protocol';
import * as SubjectActions from '../../actions/subject';

class SubjectView extends React.Component {

  componentDidMount() {
    const { dispatch } = this.props;
    const protocolId = this.props.match.params.prot_id;
    const subjectId = this.props.match.params.sub_id;

    if (!this.props.subject.activeSubject) {
      dispatch(SubjectActions.fetchSubject(protocolId, subjectId));
    }

    if (!this.props.protocol.activeProtocol) {
      dispatch(ProtocolActions.setActiveProtocol(protocolId));
    }
  }

  componentWillUnmount() {
    const { dispatch } = this.props;
    dispatch(ProtocolActions.setActiveProtocol(null));
  }
  render() {
    // Checks for empty subject state and updates it if necessary
    const subject = this.props.subject.activeSubject;
    const path = this.props.location.pathname;
    return (subject ?
      <div className="subject-view">
        <div className="row">
          <div className="col-md-4">
            <section>
              <SubjectPanel subject={subject} path={path} />
              {this.props.subject.editSubjectMode ? <SubjectCardEdit subject={subject}/> : null}
            </section>
            <hr />
            <section>
              <SubjFamPanel />
              {this.props.subjFam.addSubjFamRelMode ? <SubjFamEditView/> : null}
            </section>
          </div>
          <div className="col-md-8">
            <RecordPanel subject={subject} />
            {this.props.editLabelMode ? <EditLabelModal /> : null}
            <BackButton />
          </div>
        </div>
      </div>
      :
      <LoadingGif />
    );
  }
}

SubjectView.propTypes = {
  dispatch: PropTypes.func,
  subject: PropTypes.object,
  protocol: PropTypes.object,
  editLabelMode: PropTypes.bool,
  addSubjFamRelMode: PropTypes.bool,
  location: PropTypes.object,
  params: PropTypes.object,
};

function mapStateToProps(state) {
  return {
    protocol: {
      activeProtocol: state.protocol.activeProtocol,
      items: state.protocol.items,
    },
    subject: {
      items: state.subject.items,
      activeSubject: state.subject.activeSubject,
      editSubjectMode: state.subject.editSubjectMode,
    },
    subjFam: {
      addSubjFamRelMode: state.subjFam.addSubjFamRelMode,
    },
    editLabelMode: state.record.editLabelMode,
  };
}

export default connect(mapStateToProps)(SubjectView);
