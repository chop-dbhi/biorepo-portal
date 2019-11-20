import React from 'react';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';
import FloatingActionButton from '@material-ui/core/Button';
import RaisedButton from '@material-ui/core/Button';
import Icon from '@material-ui/core/Icon';
import NewRecordLabelSelect from './NewRecordLabelSelect';
import * as SubjectActions from '../../../../actions/subject';
import * as RecordActions from '../../../../actions/record';
import * as PDSActions from '../../../../actions/pds';
import AddButton from '../../../addButton'

class PDSRecordGroup extends React.Component {

  constructor(props) {
    super(props);
    this.handleViewRecordClick = this.handleViewRecordClick.bind(this);
    this.handleLinkRecordClick = this.handleLinkRecordClick.bind(this);
    this.handleEditRecordClick = this.handleEditRecordClick.bind(this);
    this.handleNewRecordClick = this.handleNewRecordClick.bind(this);
  }

  componentDidMount() {
    const { dispatch } = this.props;
    if (this.props.records.length === 0) {
      dispatch(PDSActions.fetchPDSLinks(this.props.pds.id));
    }
  }

  componentWillUnmount() {
    // Make sure that record state returns to its initialState once this view unmounts
    const { dispatch } = this.props;
    dispatch(RecordActions.clearRecordState());
  }

  handleRecordClick(record, pds) {
    const dispatch = this.props.dispatch;
    if (this.props.linkMode) {
      if (this.props.activeRecord.id === record.id) {
        dispatch(SubjectActions.setLinkMode());
        return;
      }
      dispatch(RecordActions.setPendingLinkedRecord(record));
    } else {
      dispatch(RecordActions.fetchRecordLinks(pds.id, this.props.subject.id, record.id));
      dispatch(RecordActions.setActiveRecord(record));
      dispatch(PDSActions.setActivePDS(pds));
    }
  }

  handleViewRecordClick() {
    const url = `/dataentry/protocoldatasource/${this.props.pds.id}/subject/` +
      `${this.props.subject.id}/record/${this.props.activeRecord.id}/start/` +
      `?p=${this.props.protocol.activeProtocolId}`;
    window.location.href = url;
  }

  handleLinkRecordClick() {
    const { dispatch } = this.props;
    dispatch(SubjectActions.setLinkMode());
  }

  handleEditRecordClick() {
    const { dispatch } = this.props;
    dispatch(RecordActions.setEditLabelMode());
  }

  handleNewRecordClick(pds) {
    const { dispatch } = this.props;
    dispatch(PDSActions.setActivePDS(pds));
    dispatch(RecordActions.setAddRecordMode(true));
  }

  isLinked(record) {
    let linked = false;
    this.props.activeLinks.forEach((link) => {
      if (link.external_record.id === record.id) {
        linked = true;
      }
    }, this);
    return linked;
  }

  Icons(props) {
  const { classes } = props;
}

  renderRecords(recordNodes) {
    return (
      recordNodes ?
        <table className="table">
          <thead>
            <tr><th>Record ID</th><th>Record</th><th>Created</th><th>Modified</th></tr>
          </thead>
          <tbody>
            {recordNodes}
          </tbody>
        </table> : <div>No Records</div>
    );
  }

  render() {
    const pds = this.props.pds;
    const records = this.props.subject.external_records.filter((record) => {
      if (pds.id === record.pds) {
        return record;
      }
      return null;
    });

    let recordNodes = null;
    const activeLinks = this.props.activeLinks;
    if (records.length !== 0) {
      recordNodes = records.map((record, i) => {
        let linkIcon = null;
        // TODO: Factor out these record lines into their own components.
        if (this.props.activeRecord != null && (this.props.activeRecord.id === record.id)) {
          return (
            <tr
              key={i}
              onClick={() => this.handleRecordClick(record, this.props.pds)}
              className="ex-rec-style"
            >
              <td>{record.id}</td>
              <td>{record.label_desc}</td>
              <td>{record.created}</td>
              <td>{record.modified}</td>
              <td className="row-action" onClick={this.handleEditRecordClick}>Label</td>
              <td className="row-action" onClick={this.handleLinkRecordClick}>Link</td>
              <td className="row-action" onClick={this.handleViewRecordClick}>View</td>
            </tr>
          );
        }
        if (activeLinks != null) {
          if (this.isLinked(record)) {
            linkIcon = <i className="ti-link"></i>;
          }
        }
        return (
          <tr
            key={i}
            onClick={() => this.handleRecordClick(record, this.props.pds)}
            className="ExternalRecord"
          >
            <td>{record.id}</td>
            <td>{linkIcon} {record.label_desc}</td>
            <td>{record.created}</td>
            <td>{record.modified}</td>
          </tr>);
      }, this);
    }

    const addButtonStyle = {
      marginLeft: '10px',
      marginTop: '10px',
      float: 'right',
    };

    return (
      <div>
        <NewRecordLabelSelect pds={this.props.pds} />
        <h5 className="category">{this.props.pds.display_label}
          {this.props.pds.authorized ?
            <div className="font-icon-wrapper" onClick={() => this.handleNewRecordClick(this.props.pds)}>
              <AddButton/>
            </div>
            : <div/>
          }
        </h5>

        <div className="PDSRecords">
          {this.props.pds.authorized ?
            this.renderRecords(recordNodes)
            : <div> Not authorized for this Protocol Data Source </div>
          }
        </div>
      </div>
    );
  }
}

PDSRecordGroup.contextTypes = {
  history: PropTypes.object,
};

PDSRecordGroup.propTypes = {
  dispatch: PropTypes.func,
  protocol: PropTypes.object,
  pds: PropTypes.object,
  record: PropTypes.object,
  records: PropTypes.array,
  subject: PropTypes.object,
  activeRecord: PropTypes.object,
  activeLinks: PropTypes.array,
  linkMode: PropTypes.bool,
  selectedLabel: PropTypes.number,
};

function mapStateToProps(state) {
  return {
    protocol: {
      items: state.protocol.items,
      activeProtocolId: state.protocol.activeProtocolId,
    },
    record: {
      isFetching: state.record.isFetching,
    },
    subject: state.subject.activeSubject,
    activeRecord: state.record.activeRecord,
    activeLinks: state.record.activeLinks,
    linkMode: state.subject.linkMode,
    selectedLabel: state.record.selectedLabel,
  };
}

export default connect(mapStateToProps)(PDSRecordGroup);
