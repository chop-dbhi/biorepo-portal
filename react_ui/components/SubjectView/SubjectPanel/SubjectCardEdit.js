// jscs:disable requireCamelCaseOrUpperCaseIdentifiers
// jscs:disable maximumLineLength
import React from 'react';
import { connect } from 'react-redux';
import RaisedButton from 'material-ui/lib/raised-button';
import SubjectTextField from './SubjectTextField';
import SubjectOrgSelectField from './SubjectOrgSelectField';
import * as SubjectActions from '../../../actions/subject';
import * as Colors from 'material-ui/lib/styles/colors';
import ExternalIDs from './ExternalIds';
import LoadingGif from '../../LoadingGif';
import moment from 'moment';

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
    this.restoreSubject();
    this.context.history.goBack();
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
    const errors = [];

    if (subject == null) {
      valid = false;
    }

    if (Object.keys(subject).length === 0) {
      valid = false;
    }

    if (!subject.organization) {
      errors.push('Organization field is required');
      valid = false;
    }

    if (!subject.first_name) {
      errors.push('First name field is required');
      valid = false;
    }

    if (!subject.last_name) {
      errors.push('Last name field is required');
      valid = false;
    }

    if (!this.validateDate(subject.dob)) {
      errors.push('DOB is required in the form YYYY-MM-DD');
      valid = false;
    }

    if (!subject.organization_subject_id) {
      errors.push('Organization subject ID is required');
      valid = false;
    }

    if (subject.organization_subject_id !== subject.organization_subject_id_validation) {
      errors.push('Organization subject IDs do not match');
      valid = false;
    }
    if (errors.length > 0) {
      dispatch(SubjectActions.setUpdateFormErrors(errors));
    }
    return valid;
  }

  renderErrors() {
    const serverErrors = this.props.subject.updateFormErrors.server;
    const formErrors = this.props.subject.updateFormErrors.form;
    const errors = serverErrors.concat(formErrors);
    const style = {
      fontSize: '12px',
      marginTop: '15px',
    };
    if (errors) {
      return errors.map((error, i) => (
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
    if (this.props.subject.activeSubject) {
      const subject = this.props.subject.activeSubject;
      return (
          <div className="card">
            <div className="more">
            </div>
            <div className="content">
              <form id="subject-form" onSubmit={this.handleSaveClick}>
                <SubjectOrgSelectField value={subject.organization} />
                <SubjectTextField
                  label={'First Name'}
                  value={subject.first_name}
                  skey={'first_name'}
                />
                <SubjectTextField
                  label={'Last Name'}
                  value={subject.last_name}
                  skey={'last_name'}
                />
                <SubjectTextField
                  label={subject.organization_id_label}
                  value={subject.organization_subject_id}
                  skey={'organization_subject_id'}
                />
                <SubjectTextField
                  label={`Verify ${subject.organization_id_label}`}
                  value={subject.organization_subject_id_validation}
                  skey={'organization_subject_id_validation'}
                />
                <SubjectTextField
                  label={'Date of Birth (YYYY-MM-DD)'}
                  value={subject.dob}
                  skey={'dob'}
                />
                <ExternalIDs externalIds={subject.external_ids} />
              {!this.props.savingSubject ?
                <div className="subject-form-button-group">
                  <RaisedButton
                    labelColor={'#7AC29A'}
                    mini
                    type="submit"
                    label={'Save'}
                  />
                  <RaisedButton
                    onClick={this.handleCancelClick}
                    labelColor={Colors.red400}
                    style={{ marginLeft: '10px' }}
                    mini
                    label={'Close'}
                  />
                </div>
                :
                <LoadingGif />
              }
              </form>
              {this.renderErrors()}
            </div>
          </div>

      );
    }
    return <div />;
  }
}

// Provides History to the SubjectCardEdit component
SubjectCardEdit.contextTypes = {
  history: React.PropTypes.object,
};

SubjectCardEdit.propTypes = {
  dispatch: React.PropTypes.func,
  protocol: React.PropTypes.object,
  subject: React.PropTypes.object,
  pds: React.PropTypes.object,
  savingSubject: React.PropTypes.bool,
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
    },
    pds: {
      items: state.pds.items,
    },
    savingSubject: state.subject.isSaving,
  };
}

export default connect(mapStateToProps)(SubjectCardEdit);
