// jscs:disable requireCamelCaseOrUpperCaseIdentifiers
import React from 'react';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';
import Select from 'react-select';
import MenuItem from '@material-ui/core/MenuItem';
import Button from 'react-bootstrap/Button';
import * as RecordActions from '../../../actions/record';
import * as Colors from '@material-ui/core/colors';

class EditLabelModal extends React.Component {

  constructor(props) {
    super(props);
    this.state = {selectedLabel: null,}
    this.handleCloseClick = this.handleCloseClick.bind(this);
    this.onChange = this.onChange.bind(this);
    this.handleRecordLabelSelect = this.handleRecordLabelSelect.bind(this);
  }

  onChange(e, index, value) {
    const record = this.props.activeRecord;
    const { dispatch } = this.props;

    const label = this.props.activePDS.driver_configuration.labels.find((lbl) => {
      if (lbl[0] === value) {
        return lbl;
      }
      return null;
    });
    record.label = this.state.selectedLabel.value;
    record.label_id = this.state.selectedLabel.value;
    record.label_desc = this.state.selectedLabel.label;
    dispatch(RecordActions.setActiveRecord(record));
    dispatch(RecordActions.updateRecord(
      this.props.activePDS.id,
      this.props.subject.id,
      record));
    dispatch(RecordActions.setEditLabelMode());
  }

  handleCloseClick() {
    const { dispatch } = this.props;
    dispatch(RecordActions.setEditLabelMode());
  }

  recordLabelOptions() {
    let labelList = null;
    let labels = this.props.activePDS.driver_configuration.labels;
    labelList = labels.map(label => ({
      value: label[0],
      label: label[1],
    }));
    return labelList
  }

  setDefaltValue(){
    let defaultValue = null;
    defaultValue = {
      value: this.props.activeRecord.label,
      label: this.props.activeRecord.label_desc,
    };
    return defaultValue
  }

  handleRecordLabelSelect(e, index, value) {
    this.setState({selectedLabel: e});
  }

  render() {
    const labels = this.props.activePDS.driver_configuration.labels;
    return (
      <section>
        <div className="backdrop-style"></div>
        <div className="col-sm-3 modal-style">
          <div className="card">
            <h6 className="category">Edit Record Label</h6>
            <div className="more">
            </div>
            <div className="content">
              <Select
                onChange={this.handleRecordLabelSelect}
                defaultValue={this.setDefaltValue()}
                options={this.recordLabelOptions()}
              />

            </div>
            <Button
              type='submit'
              size="sm"
              style={{ width: '100%' }}
              onClick={this.onChange}
            > Save </Button>
            <Button
              style={{ width: '100%' }}
              variant="danger"
              label="Cancel"
              onClick={this.handleCloseClick}
            > Cancel </Button>
          </div>
        </div>
      </section>
    );
  }
}

EditLabelModal.propTypes = {
  dispatch: PropTypes.func,
  protocol: PropTypes.object,
  subject: PropTypes.object,
  activeRecord: PropTypes.object,
  linkMode: PropTypes.bool,
  selectedLabel: PropTypes.object,
  activePDS: PropTypes.object,
};

function mapStateToProps(state) {
  return {
    protocol: {
      items: state.protocol.items,
      activeProtocol: state.protocol.activeProtocol,
    },
    subject: state.subject.activeSubject,
    activeRecord: state.record.activeRecord,
    linkMode: state.subject.linkMode,
    selectedLabel: state.record.selectedLabel,
    activePDS: state.pds.activePDS,
  };
}

export default connect(mapStateToProps)(EditLabelModal);
