// jscs:disable requireCamelCaseOrUpperCaseIdentifiers
// jscs:disable maximumLineLength
import React from 'react';
import { connect } from 'react-redux';
import { Link } from 'react-router';
import RaisedButton from 'material-ui/lib/raised-button';
import * as PedigreeActions from '../../../actions/pedigree';
import * as Colors from 'material-ui/lib/styles/colors';
import LoadingGif from '../../LoadingGif';
import SelectField from 'material-ui/lib/select-field';
import MenuItem from 'material-ui/lib/menus/menu-item';
import TextField from 'material-ui/lib/text-field';
// import moment from 'moment';

class PedigreeEditView extends React.Component {

  constructor(props) {
    super(props);
    this.handleCloseClick = this.handleCloseClick.bind(this);
  }

  restorePedigree() {
    // Restores the current Pedigree view with server's pedigree state
    const { dispatch } = this.props;

  }

  handleRelationshipSelect(e, index, value) {
    const { dispatch } = this.props;
    // dispatch(RecordActions.setSelectedRelationship(value));
  }

  handleNewpedRelClick(e) {
    const { dispatch } = this.props;
  }

  handleCloseClick() {
    // TODO: create this function - this.restorePedigree();
    const { dispatch } = this.props;
    dispatch(PedigreeActions.setAddPedigreeRelMode(false));
    // this.context.history.goBack();
  }


  isValid() {
    // validate pedigree relationship form
  }

  renderErrors() {
    //
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
    };
    const modalStyle = {
      left: '45%',
      top: '20%',
      marginLeft: '-5em',
      marginBottom: '3em',
      position: 'fixed',
      zIndex: '1000',
    };
      return (
        <section>
          <div style={backdropStyle}></div>
            <div className="col-sm-5 edit-label-modal" style={modalStyle}>
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
                        style={{ width: '100%' }}
                        value={this.props.subject.activeSubject.organization_subject_id}
                      >
                        <MenuItem primaryText={this.props.subject.activeSubject.organization_subject_id}>
                        </MenuItem>
                      </SelectField>
                    </div>
                  </row>

                  <row>
                  <div className="col-md-6">
                    <SelectField
                      floatingLabelText={'Subject Role'}
                      style={{ width: '100%' }}
                      value={this.props.subject.activeSubject.organization_subject_id}
                    >
                      <MenuItem primaryText={this.props.subject.activeSubject.organization_subject_id}>
                      </MenuItem>
                    </SelectField>
                  </div>
                  <div className="col-md-6">
                    <SelectField
                      floatingLabelText={'Related Subject Role'}
                      style={{ width: '100%' }}
                      value={this.props.subject.activeSubject.organization_subject_id}
                    >
                      <MenuItem primaryText={this.props.subject.activeSubject.organization_subject_id}>
                      </MenuItem>
                    </SelectField>
                  </div>
                  </row>
                <RaisedButton
                  onClick={this.handleNewpedRelClick}
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
              </div>
            </div>
        </section>
      );
  }
}

// Provides History to the SubjectCardEdit component
// SubjectCardEdit.contextTypes = {
//   history: React.PropTypes.object,
// };

PedigreeEditView.propTypes = {
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

export default connect(mapStateToProps)(PedigreeEditView);
