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
    const root = {

        flexGrow: 1,
        height: 250,
      };

    const backdropStyle = {
      position: 'fixed',
      top: '0px',
      left: '0px',
      width: '100%',
      height: '100%',
      zIndex: 99,
      display: 'block',
      backgroundColor: 'rgba(0, 0, 0, 0.298039)',
    };
    const cardStyle = {
      padding: '15px',
      boxShadow: '3px 3px 14px rgba(204, 197, 185, 0.5)',
      backgroundColor: 'white',
      width: '90%',
    };
    const modalStyle = {
      right: '0%',
      top: '20%',
      width: '90%',
      position: 'fixed',
      zIndex: '1000',
    };
    return (
      <section>
        <div style={backdropStyle}></div>
        <div className="col-md-12 edit-label-modal" style={modalStyle}>
          <div className="card" style={cardStyle}>
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
