import React from 'react';
import PropTypes from 'prop-types';
import Select from '@material-ui/core/Select';
import MenuItem from '@material-ui/core/MenuItem';
import RaisedButton from '@material-ui/core/Button';
import * as RecordActions from '../../../actions/record';
import * as SubjectActions from '../../../actions/subject';
import * as Colors from '@material-ui/core/colors';
import styles from './Modals.css';

import { connect } from 'react-redux';

class LinkRecord extends React.Component {

  constructor(props) {
    super(props);
    this.onChange = this.onChange.bind(this);
    this.handleLinkRecordClick = this.handleLinkRecordClick.bind(this);
    this.handleRecordLabelSelect = this.handleRecordLabelSelect.bind(this);
    this.handleNewRecordClick = this.handleNewRecordClick.bind(this);
    this.handleCloseClick = this.handleCloseClick.bind(this);
  }

  onChange(e, index, value) {
    const { dispatch } = this.props;
    dispatch(RecordActions.setSelectedLinkType(value));
  }

  handleRecordLabelSelect(e, index, value) {
    const { dispatch } = this.props;
    dispatch(RecordActions.setSelectedLabel(value));
  }

  handleNewRecordClick() {
    const { dispatch } = this.props;
    dispatch(SubjectActions.setLinkMode(false));
  }

  handleLinkRecordClick() {
    const { dispatch } = this.props;
    const activeRecord = this.props.activeRecord;
    const secondaryRecord = this.props.pendingLinkedRecord;
    if (!this.validateModal()) {
      return;
    }
    dispatch(RecordActions.createRecordLink(activeRecord, secondaryRecord));
  }

  handleCloseClick() {
    const { dispatch } = this.props;
    dispatch(RecordActions.dismissLinkModal());
    dispatch(SubjectActions.setLinkMode(false));
  }

  validateModal() {
    if (this.props.selectedLinkType == null) {
      return false;
    }
    return true;
  }

  render() {
    const primaryRecord = this.props.activeRecord;
    const secondaryRecord = this.props.pendingLinkedRecord;
    const activePds = this.props.activeRecord.pds;
    const availableLinkTypes = this.props.availableLinkTypes[activePds];
    const canLink = availableLinkTypes.length > 0;
    return (
      <section>
        <div className={styles.backdropStyle}></div>
        <div className={styles.modalStyle}>
          <div className={styles.cardStyle}>
            <h6 className="category"> Select Link Type</h6>
            <div className="more">
            </div>
            <div className="content">
              {canLink ?
                <div>
                  <div className={styles.recordStyle}>
                    <h6>
                      {primaryRecord ?
                        <span>{primaryRecord.label_desc} ID: {primaryRecord.id}</span> :
                        null}
                    </h6>
                  </div>
                  <Select
                    onChange={this.onChange}
                    value={this.props.selectedLinkType}
                    style={{ width: '100%' }}
                  >
                    {availableLinkTypes.map((link, i) => (
                      <MenuItem key={i} value={link.id} primaryText={link.desc} />
                      ))}
                  </Select>
                  <div className={styles.recordStyle}>
                    <h6>
                      {secondaryRecord ?
                        <span>{secondaryRecord.label_desc} ID: {secondaryRecord.id}</span> :
                        null
                      }
                    </h6>
                  </div>
                  {this.props.linkError != null ?
                    <div className={styles.linkErrorStyle}>Error: {this.props.linkError}</div> :
                    null
                  }
                  <RaisedButton
                    style={{ width: '100%' }}
                    labelColor={'#7AC29A'}
                    label="Link Records"
                    onClick={this.handleLinkRecordClick}
                  />
                </div>
                :
                <h6> This record is not available for linking </h6>
              }
              <RaisedButton
                style={{ width: '100%' }}
                labelColor={Colors.red400}
                label="Cancel"
                onClick={this.handleCloseClick}
              />
            </div>
          </div>
        </div>
      </section>

    );
  }
}

LinkRecord.propTypes = {
  dispatch: PropTypes.func,
  subject: PropTypes.object,
  selectedLabel: PropTypes.object,
  activeRecord: PropTypes.object,
  pendingLinkedRecord: PropTypes.object,
  selectedLinkType: PropTypes.number,
  linkError: PropTypes.string,
  availableLinkTypes: PropTypes.object,
};

function mapStateToProps(state) {
  return {
    subject: state.subject.activeSubject,
    selectedLabel: state.record.selectedLabel,
    activeRecord: state.record.activeRecord,
    pendingLinkedRecord: state.record.pendingLinkedRecord,
    selectedLinkType: state.record.selectedLinkType,
    linkError: state.record.linkError,
    availableLinkTypes: state.pds.availableLinkTypes,
  };
}

export default connect(mapStateToProps)(LinkRecord);
