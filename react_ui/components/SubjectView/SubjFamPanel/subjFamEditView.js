import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { Link } from 'react-router';

import * as SubjFamActions from '../../../actions/subjFam';
import * as SubjectActions from '../../../actions/subject';
import LoadingGif from '../../LoadingGif';
import TextField from '@material-ui/core/TextField';
import FormControl from '@material-ui/core/FormControl';
// import Button from '@material-ui/core/Button';

import { Container, Row, Col } from 'reactstrap';
import Select from 'react-select';
import Button from 'react-bootstrap/Button'


class SubjFamEditView extends React.Component {

  constructor(props) {
    super(props);

    this.state = {
      relatedSubject: '',
      subjectRole: '',
      relatedSubjectRole: '',
      dataEntryCorrect: '',
      relatedSubErr: false,
      subjectRoleError: false,
      relatedSubRoleErr: false

    };
    this.handleRelatedSubjectSelect = this.handleRelatedSubjectSelect.bind(this);
    this.handleSubject1RoleSelect = this.handleSubject1RoleSelect.bind(this);
    this.handleSubject2RoleSelect = this.handleSubject2RoleSelect.bind(this);
    this.handleCloseClick = this.handleCloseClick.bind(this);
    this.handleNewPedRelClick = this.handleNewPedRelClick.bind(this);
    this.checkRelDataEntry = this.checkRelDataEntry.bind(this);
  }

  menuItemsSubjects(){
    let subjectList = null;
    const subjects = this.props.subject.items;
    if(subjects !=null){
      subjectList = subjects.map(subject =>({
          value: subject.id,
          label: subject.organization_subject_id + " - " + subject.last_name +
            ", " + subject.first_name,
        }));
    }
    else{
      subjectList = <option primaryText={this.props.subject.activeSubject.organization_subject_id}>{this.props.subject.activeSubject.organization_subject_id}
      </option>;
    }
    return subjectList;
  }

  menuItemsRelTypes(){
    let relTypeList = null;
    const relTypes = this.props.relTypes[0];
    relTypeList = relTypes.map(relType =>({
        value: relType.id,
        label: relType.desc,
      }));
    return relTypeList;
  }

  restoreSubjFam() {
    // Restores the current SubjFam view with server's SubjFam state
    const { dispatch } = this.props;
  }

  handleRelatedSubjectSelect(e, index, value) {
    this.setState({relatedSubject: e});
  }

  handleSubject1RoleSelect(e, index, value){
    this.setState({subjectRole: e});
  }

  handleSubject2RoleSelect(e, index, value){
    this.setState({relatedSubjectRole: e});
  }

  checkRelDataEntry(){
    const { dispatch } = this.props;
    if (this.state.relatedSubject == '') {
      this.setState({relatedSubErr: true});
    } else {
      this.setState({relatedSubErr: false });
    }

    if (this.state.subjectRole == '') {
      this.setState({subjectRoleError: true});
    } else {
      this.setState({subjectRoleError: false});
    }

    if (this.state.relatedSubjectRole == '') {
      this.setState({relatedSubRoleErr: true});
    } else {
      this.setState({relatedSubRoleErr: false});
    }

    if(this.state.relatedSubject == '' || this.state.subjectRole == '' || this.state.relatedSubjectRole == ''){
      this.setState({dataEntryCorrect: false})
      return false;
    } else {
      this.setState({dataEntryCorrect: true});
      return true;
    }



  }
  handleNewPedRelClick(e) {
    const { dispatch } = this.props;
    if (this.checkRelDataEntry()) {
      const newRel = {
          "subject_1": this.props.subject.activeSubject.id,
          "subject_2": this.state.relatedSubject.value,
          "subject_1_role": this.state.subjectRole.value,
          "subject_2_role": this.state.relatedSubjectRole.value,
          "protocol_id": this.props.protocol.activeProtocolId,
      }
      dispatch(SubjFamActions.addSubjFamRel(this.props.protocol.activeProtocolId, newRel))
      .then(dispatch(SubjFamActions.fetchSubjFam(this.props.protocol.activeProtocolId, newRel.subject_1)))
      this.handleCloseClick();
    }
  }

  handleCloseClick() {
    const { dispatch } = this.props;
    dispatch(SubjFamActions.setAddSubjFamRelMode(false));
  }

  renderErrors() {

  }

  render() {
    // options for the select forms
    const subjects = this.menuItemsSubjects();
    const relTypes = this.menuItemsRelTypes();

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

    const errorStyle = {
      control: styles => ({ ...styles, backgroundColor: 'pink' })
    }

    const { value } = this.state;
      return (
        <section>

          <div style={backdropStyle}></div>
            <div className="col-md-12 edit-label-modal" style={modalStyle}>
              <div className="card" style={cardStyle}>
                <h3 className="category" style={{ textAlign: 'center' }}> Add a new Relationship </h3>
                  <Row>
                    <div className="col-md-6">
                      <label> Subject: </label>
                      <TextField
                        style={{ width: '100%', whiteSpace: 'nowrap',  fontSize: '16'}}
                        value={this.props.subject.activeSubject.organization_subject_id}
                      />
                      </div>
                      <div className="col-md-6">
                      <label> Related Subject: </label>
                        <Select
                          onChange={this.handleRelatedSubjectSelect}
                          error={this.state.dataEntryCorrect}
                          value={this.state.relatedSubject}
                          placeholder="Search for Related Subject"
                          styles={this.state.relatedSubErr ? errorStyle : {}}
                          options={subjects}
                        />
                        {this.state.relatedSubErr ? <p>Please select related subject. </p> : null}
                      </div>
                    </Row>
                    <Row>
                      <div className="col-md-6">
                        <label> Subject Role: </label>
                        <Select
                          styles={this.state.subjectRoleError ? errorStyle : {}}
                          value={this.state.subjectRole}
                          onChange={this.handleSubject1RoleSelect}
                          options={relTypes}
                          placeholder="Search for Subject Role Types"
                        />
                      {this.state.subjectRoleError ? <p>Please select subject role. </p> : null}

                      </div>

                      <div className="col-md-6">
                        <label> Related Subject Role: </label>
                        <Select
                          options={relTypes}
                          styles={this.state.relatedSubRoleErr ? errorStyle : {}}
                          value={this.state.relatedSubjectRole}
                          onChange={this.handleSubject2RoleSelect}
                          placeholder="Search for Related Subject Role Types"
                        />
                        {this.state.relatedSubRoleErr ? <p>Please select related subject role. </p> : null}

                        </div>
                    </Row>
                  <Row>
                    <center>

                      <Button
                        label={'Create New'}
                        type='submit'
                        size="sm"
                        onClick={this.handleNewPedRelClick}
                      > Create New </Button>

                      <Button
                        variant="contained"
                        onClick={this.handleCloseClick}
                        type='reset'
                        variant="danger"
                        size="sm"
                      > Cancel </Button>
                    {this.props.updateFormErrors != null ?
                      <div className="alert alert-danger">{this.props.updateFormErrors}</div>
                    : null}
                  </center>
                </Row>
              </div>
            </div>
        </section>
      );
    }
  }


SubjFamEditView.propTypes = {
  dispatch: PropTypes.func,
  protocol: PropTypes.object,
  subject: PropTypes.object,
  pds: PropTypes.object,
  savingSubject: PropTypes.bool,
  relTypes: PropTypes.array,
  updateFormErrors: PropTypes.string,
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
    updateFormErrors: state.subjFam.updateFormErrors
  };
}

export default connect(mapStateToProps)(SubjFamEditView);
