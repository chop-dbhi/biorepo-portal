import React from 'react';
import { connect } from 'react-redux';
import { Link } from 'react-router';
import RaisedButton from 'material-ui/lib/raised-button';
import * as SubjFamActions from '../../../actions/subjFam';
import * as SubjectActions from '../../../actions/subject';
import * as Colors from 'material-ui/lib/styles/colors';
import LoadingGif from '../../LoadingGif';
import SelectField from 'material-ui/lib/select-field';
import MenuItem from 'material-ui/lib/menus/menu-item';
import TextField from 'material-ui/lib/text-field';

class SubjFamEditView extends React.Component {

  constructor(props) {
    super(props);

    this.state = {
      relatedSubject: '',
      subjectRole: '',
      relatedSubjectRole: '',
      dataEntryCorrect: '',
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
      subjectList =
        subjects.map((subject, i) => (
          <MenuItem key={i} value={subject.id} primaryText={subject.organization_subject_id} />
        ));
    }
    else{
      subjectList = <MenuItem primaryText={this.props.subject.activeSubject.organization_subject_id}>
      </MenuItem>;

    }
    return subjectList;
  }

  menuItemsRelTypes(){
    let relTypeList = null;
    const relTypes = this.props.relTypes[0];
    console.log(relTypes)
    relTypeList =
      relTypes.map((rel, i) => (
        <MenuItem key={i} value={rel.id} primaryText={rel.desc} />
      ))

      return relTypeList;
  }

  restoreSubjFam() {
    // Restores the current SubjFam view with server's SubjFam state
    const { dispatch } = this.props;
  }

  handleRelatedSubjectSelect(e, index, value) {
    this.setState({relatedSubject: value});
  }

  handleSubject1RoleSelect(e, index, value){
    this.setState({subjectRole: value});
  }

  handleSubject2RoleSelect(e, index, value){
    this.setState({relatedSubjectRole: value});
  }

  checkRelDataEntry(){
    const { dispatch } = this.props;
    if (this.state.relatedSubject == '') {
      dispatch(SubjFamActions.setUpdateFormErrors("please select related subject"))
      this.setState({dataEntryCorrect: false});
      return false;
    }
    if (this.state.subjectRole == '') {
      dispatch(SubjFamActions.setUpdateFormErrors("please select subject role"))
      this.setState({dataEntryCorrect: false});
      return false;
    }
    if (this.state.relatedSubjectRole == '') {
      dispatch(SubjFamActions.setUpdateFormErrors("please select related subject role"))
      this.setState({dataEntryCorrect: false});
      return false;
    }
    else
      console.log("related subject does not equal ''")
      this.setState({dataEntryCorrect: true});
      console.log(this.state.dataEntryCorrect);
      return true;
  }
  handleNewPedRelClick(e) {
    console.log("we are in handleNewPedRelClick")
    const { dispatch } = this.props;
    console.log(this.state.dataEntryCorrect)
    if (this.checkRelDataEntry()) {
      console.log(this.state.dataEntryCorrect)
      const newRel = {
          "subject_1": this.props.subject.activeSubject.id,
          "subject_2": this.state.relatedSubject,
          "subject_1_role": this.state.subjectRole,
          "subject_2_role": this.state.relatedSubjectRole,
          "protocol_id": this.props.protocol.activeProtocolId,
      }
      dispatch(SubjFamActions.addSubjFamRel(this.props.protocol.activeProtocolId, newRel))
      .then(dispatch(SubjFamActions.fetchSubjFam(this.props.protocol.activeProtocolId, newRel.subject_1)))
    }
  }

  handleCloseClick() {
    const { dispatch } = this.props;
    dispatch(SubjFamActions.setAddSubjFamRelMode(false));
  }

  renderErrors() {

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
    const { value } = this.state;
      return (
        <section>
          <div style={backdropStyle}></div>
            <div className="col-md-12 edit-label-modal" style={modalStyle}>
              <div className="card" style={cardStyle}>
                <h3 className="category" style={{ textAlign: 'center' }}> Add a new Relationship </h3>
                  <row>
                  <div className="col-md-6">
                    <TextField
                      style={{ width: '100%', whiteSpace: 'nowrap' }}
                      value={this.props.subject.activeSubject.organization_subject_id}
                      floatingLabelText={'Subject'}
                    />
                    </div>
                    <div className="col-md-6">
                      <SelectField
                        floatingLabelText={'Related Subject'}
                        onChange={this.handleRelatedSubjectSelect}
                        error={this.state.dataEntryCorrect}
                        style={{ width: '100%' }}
                        value={this.state.relatedSubject}
                      >
                      {this.menuItemsSubjects()}
                      </SelectField>
                    </div>
                  </row>
                  <row>
                  <div className="col-md-6">
                    <SelectField
                      floatingLabelText={'Subject Role'}
                      style={{ width: '100%',  }}
                      value={this.state.subjectRole}
                      onChange={this.handleSubject1RoleSelect}
                    >
                      {this.menuItemsRelTypes()}
                    </SelectField>
                  </div>
                  <div className="col-md-6">
                    <SelectField
                      floatingLabelText={'Related Subject Role'}
                      style={{ width: '100%', overflowWrap: 'normal'}}
                      value={this.state.relatedSubjectRole}
                      onChange={this.handleSubject2RoleSelect}
                    >
                    {this.menuItemsRelTypes()}
                    </SelectField>
                  </div>
                  </row>
                <RaisedButton
                  onClick={this.handleNewPedRelClick}
                  label={'Create New'}
                  labelColor={'#7AC29A'}
                  type="submit"
                  style={{ width: '100%' }}
                />
                <RaisedButton
                  style={{ width: '100%' }}
                  labelColor={Colors.red400}
                  label="Cancel"
                  onClick={this.handleCloseClick}
                />
                {this.props.updateFormErrors != null ?
                  <div className="alert alert-danger">{this.props.updateFormErrors}</div>
                : null}
              </div>
            </div>
        </section>
      );
  }
}

SubjFamEditView.propTypes = {
  dispatch: React.PropTypes.func,
  protocol: React.PropTypes.object,
  subject: React.PropTypes.object,
  pds: React.PropTypes.object,
  savingSubject: React.PropTypes.bool,
  relTypes: React.PropTypes.array,
  updateFormErrors: React.PropTypes.string,
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
