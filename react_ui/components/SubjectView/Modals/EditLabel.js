// jscs:disable requireCamelCaseOrUpperCaseIdentifiers
import React from 'react';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';
import Select from '@material-ui/core/Select';
import MenuItem from '@material-ui/core/MenuItem';
import RaisedButton from '@material-ui/core/Button';
import * as RecordActions from '../../../actions/record';
import * as Colors from '@material-ui/core/colors';
import styles from './Modals.css';

class EditLabelModal extends React.Component {

  constructor(props) {
    super(props);
    this.handleCloseClick = this.handleCloseClick.bind(this);
    this.onChange = this.onChange.bind(this);
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
    record.label = label[0];
    record.label_id = label[0];
    record.label_desc = label[1];
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

  render() {
    const labels = this.props.activePDS.driver_configuration.labels;
  
    return (
      <section>
        <div className={styles.backdropStyle}></div>
        <div className={styles.editLabelModalStyle}>
          <div className={styles.cardStyle}>
            <h6 className="category">Edit Record Label</h6>
            <div className="more">
            </div>
            <div className="content">
              <Select
                style={{ width: '100%' }}
                onChange={this.onChange}
                value={this.props.activeRecord.label}
              >
                {labels.map((label, i) => (
                  <MenuItem key={i} value={label[0]}>{label[1]}</MenuItem>))
                }
              </Select>
            </div>
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
