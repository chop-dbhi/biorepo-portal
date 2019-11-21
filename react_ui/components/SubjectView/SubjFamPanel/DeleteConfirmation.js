import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { Container, Row, Col } from 'reactstrap';
import Button from 'react-bootstrap/Button'

import * as SubjFamActions from '../../../actions/subjFam';
import * as SubjectActions from '../../../actions/subject';
import { organizeSubjFamRelForEdit, handleRelEditDelCloseClick } from '../../utils'

class DeleteConfirmation extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
        relatedSubject: this.props.activeSubjFam.related_subject_org_id,
        relatedSubjectId: this.props.activeSubjFam.related_subject_id,
        subjectRole: this.props.activeSubjFam.subject_role,
        relatedSubjectRole: this.props.activeSubjFam.related_subject_role,
    };
    this.handleRelEditDelCloseClick = handleRelEditDelCloseClick.bind(this);
    this.handleDeleteSubjRel = this.handleDeleteSubjRel.bind(this);
    this.organizeSubjFamRelForEdit = organizeSubjFamRelForEdit.bind(this);
      }

  handleDeleteSubjRel() {
    const { dispatch } = this.props;
    let subjFamRelToDelete = this.organizeSubjFamRelForEdit()
    dispatch(SubjFamActions.fetchDeleteSubjFamRel(this.props.protocol.activeProtocolId,
                                                  subjFamRelToDelete,
                                                  this.props.subject.activeSubject.id))
    .then(dispatch(SubjFamActions.setDeleteSubjFamRelMode(false)))
    .then(dispatch(SubjFamActions.fetchSubjFam(this.props.protocol.activeProtocolId, this.props.subject.activeSubject.id)));
  }

  render() {
    return (
      <section>
        <div className="backdrop-style"></div>
        <div className="col-md-12 subj-fam-modal-style">
          <div className="card">
            <h3 className="category" style={{ textAlign: 'center' }}> Are you Sure you want to delete this relationship? </h3>
            <Row>
              <div className="col-md-6">
                <label> Subject: {this.props.subject.activeSubject.organization_subject_id}</label>
              </div>
              <div className="col-md-6">
                <label> Related Subject: {this.state.relatedSubject}</label>
              </div>
            </Row>
            <Row>
              <div className="col-md-6">
                <label> Subject Role: {this.state.subjectRole}</label>
              </div>
              <div className="col-md-6">
                <label> Related Subject Role: {this.state.relatedSubjectRole}</label>
              </div>
            </Row>
            <Row>
              <center>
                <Button
                  label={'Create New'}
                  type='submit'
                  size="sm"
                  onClick={this.handleDeleteSubjRel}
                > Delete </Button>
                <Button
                  variant="contained"
                  onClick={this.handleRelEditDelCloseClick}
                  type='reset'
                  variant="danger"
                  size="sm"
                > Cancel </Button>
              </center>
            </Row>
          </div>
        </div>
      </section>
      );
  }
}

DeleteConfirmation.propTypes = {
  dispatch: PropTypes.func,
  protocol: PropTypes.object,
  subject: PropTypes.object,
  pds: PropTypes.object,
  savingSubject: PropTypes.bool,
  relTypes: PropTypes.array,
  updateFormErrors: PropTypes.string,
  activeSubjFam: PropTypes.object,
  editSubjFamRelMode: PropTypes.bool,
  deleteSubjFamRelMode: PropTypes.bool,
};

function mapStateToProps(state) {
  return {
    protocol: {
      items: state.protocol.items,
      activeProtocolId: state.protocol.activeProtocolId,
      orgs: state.protocol.orgs,
    },
    subject: {
      items: state.subject.items,
      activeSubject: state.subject.activeSubject,
    },
    pds: {
      items: state.pds.items,
    },
    savingSubject: state.subject.isSaving,
    relTypes: state.subjFam.relTypes,
    updateFormErrors: state.subjFam.updateFormErrors,
    activeSubjFam: state.subjFam.activeSubjFam,
    editSubjFamRelMode: state.subjFam.editSubjFamRelMode,
    deleteSubjFamRelMode: state.subjFam.deleteSubjFamRelMode
  };
}

export default connect(mapStateToProps)(DeleteConfirmation);
