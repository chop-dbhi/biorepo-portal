// jscs:disable requireCamelCaseOrUpperCaseIdentifiers
// jscs:disable maximumLineLength
import React from 'react';
import { connect } from 'react-redux';
import BackButton from '../BackButton';
import LoadingGif from '../LoadingGif';
import SubjectPanel from './SubjectPanel';
import RecordPanel from './RecordPanel';
import SubjFamPanel from './SubjFamPanel'
import EditLabelModal from './Modals/EditLabel';
import SubjFamEditView from './SubjFamPanel/subjFamEditView';
import * as ProtocolActions from '../../actions/protocol';
import * as SubjectActions from '../../actions/subject';

class SubjectView extends React.Component {

  componentDidMount() {
    const { dispatch } = this.props;
    const protocolId = this.props.params.prot_id;
    const subjectId = this.props.params.sub_id;

    if (!this.props.subject.activeSubject) {
      dispatch(SubjectActions.fetchSubject(protocolId, subjectId));
    }

    if (!this.props.protocol.activeProtocol) {
      dispatch(ProtocolActions.fetchProtocol(protocolId));
    }
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
              <SubjectPanel subject={subject} edit={this.props.params.edit} path={path} />
            </section>
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
  dispatch: React.PropTypes.func,
  subject: React.PropTypes.object,
  protocol: React.PropTypes.object,
  editLabelMode: React.PropTypes.bool,
  addSubjFamRelMode: React.PropTypes.bool,
  location: React.PropTypes.object,
  params: React.PropTypes.object,
};

function mapStateToProps(state) {
  return {
    protocol: {
      activeProtocol: state.protocol.activeProtocol,
    },
    subject: {
      items: state.subject.items,
      activeSubject: state.subject.activeSubject,
    },
    subjFam: {
      addSubjFamRelMode: state.subjFam.addSubjFamRelMode,
    },
    editLabelMode: state.record.editLabelMode,
  };
}

export default connect(mapStateToProps)(SubjectView);
