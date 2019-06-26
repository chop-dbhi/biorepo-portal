// jscs:disable requireCamelCaseOrUpperCaseIdentifiers
// jscs:disable maximumLineLength
import React from 'react';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';
import RaisedButton from '@material-ui/core/Button';
import SubjectTextField from './SubjectTextField';
import SubjectOrgSelectField from './SubjectOrgSelectField';
import SubjectDOBField from './SubjectDOBField';
import * as SubjectActions from '../../../actions/subject';
import * as Colors from '@material-ui/core/colors';
import ExternalIDs from './ExternalIds';
import LoadingGif from '../../LoadingGif';
import moment from 'moment';
import Button from 'react-bootstrap/Button'
import PureModal from 'react-pure-modal';
import 'react-pure-modal/dist/react-pure-modal.min.css';

class SubjectCardEdit extends React.Component {

  constructor(props) {
    super(props);
    this.handleCancelClick = this.handleCancelClick.bind(this);
    this.handleSaveClick = this.handleSaveClick.bind(this);
  }

  restoreSubject() {
    // Restores the current Subject view with server's subject state
    const { dispatch } = this.props;
    const activeProtocolId = this.props.protocol.activeProtocolId;
    const activeSubjectId = this.props.subject.activeSubject.id;
    dispatch(SubjectActions.fetchSubject(activeProtocolId, activeSubjectId));
  }

  handleSaveClick(e) {
    const { dispatch } = this.props;
    const protocolId = this.props.protocol.activeProtocolId;
    const subject = this.props.subject.activeSubject;
    if (this.isValid()) {
      dispatch(SubjectActions.updateSubject(protocolId, subject));
    }
    e.preventDefault();
  }

  handleCancelClick() {
    const { dispatch } = this.props;
    this.restoreSubject();
    dispatch(SubjectActions.setEditSubjectMode(false));
  }

  validateDate(date) {
    if (!moment(date, ['YYYY-MM-DD']).isValid()) {
      return false;
    }
    if (!/^\d{4}-\d{1,2}-\d{1,2}$/.test(date)) {
      return false;
    }
    if (date === '') {
      return false;
    }
    return true;
  }

  isValid() {
    const subject = this.props.subject.activeSubject;
    const { dispatch } = this.props;

    let valid = true;
    let new_errs= [];

    if (subject == null) {
      valid = false;
    }
    if (Object.keys(subject).length === 0) {
      valid = false;
    }

    if (!subject.organization) {
      new_errs['orgRequired']= 'Organization field is required.';
      valid = false;
    }

    if (!subject.first_name) {
      new_errs['fnReq']= 'First name field is required.';

      valid = false;
    }

    if (!subject.last_name) {
      new_errs['lnReq']= 'Last name field is required.';

      valid = false;
    }

    if(!subject.dob){
      new_errs['dobR']= 'Date of birth field is required.'
      valid = false;
    }else if (!this.validateDate(subject.dob)) {
      new_errs['dobR']= 'Must be a valid date (YYYY-MM-DD).';
      valid = false;
    }
    if (!subject.organization_subject_id) {
      new_errs['oidReq']= 'Organization subject ID is required.';

      valid = false;
    }
    if(!subject.organization_subject_id_validation){
      new_errs['oidNoMatch'] = 'Organization subject ID verification is required.';
      valid = false;
    } else if (subject.organization_subject_id !== subject.organization_subject_id_validation) {
      new_errs['oidNoMatch']= 'Organization subject IDs do not match.';

      valid = false;
    }
    dispatch(SubjectActions.setUpdateFormErrors(new_errs));
    return valid;
  }

  renderErrors() {
    const serverErrors = this.props.subject.updateFormErrors.server;
    const style = {
      fontSize: '12px',
      marginTop: '15px',
    };
    if (serverErrors) {
      return serverErrors.map((error, i) => (
        <div key={i} style={style} className="alert alert-danger">
          <div className="container">
            {error}
          </div>
        </div>
        )
      );
    }
    return null;
  }

  render() {

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

    if (this.props.subject.activeSubject) {
      const subject = this.props.subject.activeSubject;
      return (
        <section>
          <div style={backdropStyle}/>
              <PureModal
                isOpen
                width='500px'
                onClose={() => {return false;}}
                >
                <div className="card">
                  <h6 className="category"><center>Edit Subject</center></h6>
                  <div className="more"/>
                    <div className="content">
                      <form id="subject-form" onSubmit={this.handleSaveClick}>
                        <SubjectOrgSelectField
                          value={subject.organization}
                          label={subject.organization_name}
                          error={this.props.subject.updateFormErrors.form['orgRequired']}

                        />
                        <SubjectTextField
                          label={'First Name'}
                          value={subject.first_name}
                          skey={'first_name'}
                          error={this.props.subject.updateFormErrors.form['fnReq']}

                        />
                        <SubjectTextField
                          label={'Last Name'}
                          value={subject.last_name}
                          skey={'last_name'}
                          error={this.props.subject.updateFormErrors.form['lnReq']}

                        />
                        <SubjectTextField
                          label={subject.organization_id_label}
                          value={subject.organization_subject_id}
                          skey={'organization_subject_id'}
                          error={this.props.subject.updateFormErrors.form['oidReq']}

                        />
                        <SubjectTextField
                          label={`Verify ${subject.organization_id_label}`}
                          value={subject.organization_subject_id_validation}
                          skey={'organization_subject_id_validation'}
                          error={this.props.subject.updateFormErrors.form['oidNoMatch']}

                        />
                        <SubjectDOBField
                          value={subject.dob}
                          error={this.props.subject.updateFormErrors.form['dobR']}
                        />
                        <ExternalIDs externalIds={subject.external_ids} />
                      {!this.props.savingSubject ?
                        <div className="subject-form-button-group">
                          <Button
                            labelcolor={'#7AC29A'}
                            type="submit"
                            label={'Save'} > Save </Button>

                          <Button
                            onClick={this.handleCancelClick}
                            variant="danger"
                            style={{ marginLeft: '10px' }}
                            label={'Close'}> Cancel </Button>
                        </div>
                  :
                  <LoadingGif />
                }
                </form>
                {this.renderErrors()}
              </div>
            </div>
          </PureModal>

    </section>
    );
    }
    return <div />;
  }
}

// Provides History to the SubjectCardEdit component
SubjectCardEdit.contextTypes = {
  history: PropTypes.object,
};

SubjectCardEdit.propTypes = {
  dispatch: PropTypes.func,
  protocol: PropTypes.object,
  subject: PropTypes.object,
  pds: PropTypes.object,
  savingSubject: PropTypes.bool,
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
      updateFormErrors: state.subject.updateFormErrors,
      editSubjectMode: state.subject.editSubjectMode,
    },
    pds: {
      items: state.pds.items,
    },
    savingSubject: state.subject.isSaving,
  };
}

export default connect(mapStateToProps)(SubjectCardEdit);
