// jscs:disable requireCamelCaseOrUpperCaseIdentifiers
// jscs:disable maximumLineLength
import React from 'react';
import { connect } from 'react-redux';
import { Link } from 'react-router';
import RaisedButton from 'material-ui/lib/raised-button';
import * as PedigreeActions from '../../../actions/pedigree';
import * as Colors from 'material-ui/lib/styles/colors';
import LoadingGif from '../../LoadingGif';
import moment from 'moment';

class SubjectCardEdit extends React.Component {

  constructor(props) {
    super(props);

  }

  restorePedigree() {
    // Restores the current Pedigree view with server's pedigree state
    const { dispatch } = this.props;

  }

  handleSaveClick(e) {
    const { dispatch } = this.props;
  }

  handleCancelClick() {
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
                    <h4> Subject     ___________   Related Subject      _____________ </h4>
                  </row>
                  <row>
                    <h4> Subject Role___________   Related subject Role _____________ </h4>
                  </row>
                <RaisedButton
                  onMouseUp={this.handleNewRecordClick}
                  label={'Create New'}
                  labelColor={'#7AC29A'}
                  type="submit"
                  style={{ width: '100%' }}
                />
                <RaisedButton
                  style={{ width: '100%' }}
                  labelColor={Colors.red400}
                  label="Cancel"
                  onMouseUp={this.handleCancelClick}
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
