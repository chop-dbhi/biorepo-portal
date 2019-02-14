// jscs:disable requireCamelCaseOrUpperCaseIdentifiers
import React from 'react';
import PropTypes from 'prop-types';
import Select from '@material-ui/core/Select';
import MenuItem from '@material-ui/core/MenuItem';
import RaisedButton from '@material-ui/core/Button';
import LoadingGif from '../../../LoadingGif';
import * as RecordActions from '../../../../actions/record';
import * as Colors from '@material-ui/core/colors';

import { connect } from 'react-redux';

class NewRecordLabelSelect extends React.Component {

  constructor(props) {
    super(props);
    this.handleRecordLabelSelect = this.handleRecordLabelSelect.bind(this);
    this.handleNewRecordClick = this.handleNewRecordClick.bind(this);
    this.handleCloseClick = this.handleCloseClick.bind(this);
  }

  handleRecordLabelSelect(e, index, value) {
    const { dispatch } = this.props;
    dispatch(RecordActions.setSelectedLabel(value));
  }

  handleNewRecordClick() {
    const { dispatch } = this.props;
    if (this.props.selectedLabel === null) {
      dispatch(RecordActions.setRecordError('Please select a record label.'));
      return;
    }
    dispatch(RecordActions.createRecordRequest());
    const url = `/dataentry/protocoldatasource/${this.props.pds.id}/subject/` +
      `${this.props.subject.id}/create/?label_id=${this.props.selectedLabel}`;
    window.location.href = url;
  }

  handleCloseClick() {
    const { dispatch } = this.props;
    dispatch(RecordActions.setAddRecordMode(false));
  }

  render() {
    const labels = this.props.pds.driver_configuration.labels;
    const modalStyle = {
      left: '45%',
      top: '20%',
      marginLeft: '-5em',
      marginBottom: '3em',
      position: 'fixed',
      zIndex: '1000',
    };
    const cardStyle = {
      padding: '15px',
      boxShadow: '3px 3px 14px rgba(204, 197, 185, 0.5)',
      backgroundColor: 'white',
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
    return (
      this.props.isCreating && this.props.pds.id == this.props.activePDS.id ?
        <section>
          <div style={backdropStyle}></div>
          <div className="col-sm-3 edit-label-modal" style={modalStyle}>
            <div className="card" style={cardStyle}>
              <h4 style={{ textAlign: 'center' }}>
                Please wait. This action may take several seconds...
              </h4>
              <LoadingGif />
            </div>
          </div>
        </section> :
          this.props.addRecordMode && this.props.pds.id == this.props.activePDS.id ?
            <section>
              <div style={backdropStyle}></div>
              <div className="col-sm-3 edit-label-modal" style={modalStyle}>
                <div className="card" style={cardStyle}>
                  <h6 className="category">Select label for {this.props.pds.display_label} Record</h6>
                  <div className="more">
                  </div>
                  <div className="content">
                    <Select
                      onChange={this.handleRecordLabelSelect}
                      style={{ width: '100%' }}
                      value={this.props.selectedLabel}
                    >
                      {labels.map((label, i) => (
                        <MenuItem key={i} value={label[0]} primaryText={label[1]} />
                      ))}
                    </Select>
                  </div>
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
                    onMouseUp={this.handleCloseClick}
                  />
                  {this.props.newRecordError != null ?
                    <div className="alert alert-danger">{this.props.newRecordError}</div>
                  : null}
                </div>
              </div>
            </section>


          : null

    );
  }
}

NewRecordLabelSelect.propTypes = {
  dispatch: PropTypes.func,
  subject: PropTypes.object,
  selectedLabel: PropTypes.number,
  pds: PropTypes.object,
  isCreating: PropTypes.bool,
  newRecordError: PropTypes.string,
};

function mapStateToProps(state) {
  return {
    activePDS: state.pds.activePDS,
    subject: state.subject.activeSubject,
    selectedLabel: state.record.selectedLabel,
    isCreating: state.record.isCreating,
    newRecordError: state.record.newRecordError,
    addRecordMode: state.record.addRecordMode,
  };
}

export default connect(mapStateToProps)(NewRecordLabelSelect);
