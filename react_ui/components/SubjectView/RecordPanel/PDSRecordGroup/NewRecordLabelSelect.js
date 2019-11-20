// jscs:disable requireCamelCaseOrUpperCaseIdentifiers
import React from 'react';
import PropTypes from 'prop-types';
import MenuItem from '@material-ui/core/MenuItem';
import LoadingGif from '../../../LoadingGif';
import * as RecordActions from '../../../../actions/record';
import * as Colors from '@material-ui/core/colors';
import Button from 'react-bootstrap/Button';
import Select from 'react-select';

import { connect } from 'react-redux';

class NewRecordLabelSelect extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      selectedLabel: null,
      recordLabelSelectError: false
  };
    this.handleRecordLabelSelect = this.handleRecordLabelSelect.bind(this);
    this.handleNewRecordClick = this.handleNewRecordClick.bind(this);
    this.handleCloseClick = this.handleCloseClick.bind(this);
  }

  recordLabelOptions() {
    let labelList = null;
    let labels = this.props.pds.driver_configuration.labels
    labelList = labels.map(label => ({
      value: label[0],
      label: label[1],
    }));
    return labelList
  }

  handleRecordLabelSelect(e, index, value) {
    const { dispatch } = this.props;
    this.setState({selectedLabel: e});
  }

  handleNewRecordClick() {
    const { dispatch } = this.props;
    if (this.state.selectedLabel == null) {
        this.setState({recordLabelSelectError: true})
      return;
    } else {
      this.setState({recordLabelSelectError: false})
    }
    dispatch(RecordActions.createRecordRequest());
    const url = `/dataentry/protocoldatasource/${this.props.pds.id}/subject/` +
      `${this.props.subject.id}/create/?label_id=${this.state.selectedLabel.value}`;
    window.location.href = url;
  }

  handleCloseClick() {
    const { dispatch } = this.props;
    dispatch(RecordActions.setAddRecordMode(false));
  }

  render() {
    const labels = this.props.pds.driver_configuration.labels;
    const errorStyle = {
      control: styles => ({ ...styles, backgroundColor: 'pink' })
    }
    return (
      this.props.isCreating && this.props.pds.id == this.props.activePDS.id ?
        <section>
          <div className="backdrop-style"></div>
          <div className="col-sm-3 edit-label-modal-style">
            <div className="card">
              <h4 style={{ textAlign: 'center' }}>
                Please wait. This action may take several seconds...
              </h4>
              <LoadingGif />
            </div>
          </div>
        </section> :
          this.props.addRecordMode && this.props.pds.id == this.props.activePDS.id ?
            <section>
              <div className="backdrop-style"></div>
              <div className="col-sm-3 edit-label-modal-style">
                <div className="card">
                  <h6 className="category">Select label for {this.props.pds.display_label} Record</h6>
                  <div className="more">
                  </div>
                  <div className="content">
                    <Select
                      onChange={this.handleRecordLabelSelect}
                      styles={this.state.recordLabelSelectError ? errorStyle: {}}
                      value={this.state.selectedLabel}
                      options={this.recordLabelOptions()}
                      placeholder="Search for record label"

                    />
                    {this.state.recordLabelSelectError ?
                     <p>Select a record label.</p> : null}
                  </div>
                  <Button
                    type='submit'
                    size="sm"
                    style={{ width: '100%' }}
                    onClick={this.handleNewRecordClick}
                  > Create New </Button>
                  <Button
                    style={{ width: '100%' }}
                    variant="danger"
                    type='cancel'
                    size="sm"
                    label="Cancel"
                    onMouseUp={this.handleCloseClick}
                  > Cancel </Button>

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
};

function mapStateToProps(state) {
  return {
    activePDS: state.pds.activePDS,
    subject: state.subject.activeSubject,
    selectedLabel: state.record.selectedLabel,
    isCreating: state.record.isCreating,
    addRecordMode: state.record.addRecordMode,
  };
}

export default connect(mapStateToProps)(NewRecordLabelSelect);
