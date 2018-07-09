import React from 'react';
import { connect } from 'react-redux';
import FloatingActionButton from 'material-ui/lib/floating-action-button';
import RaisedButton from 'material-ui/lib/raised-button';
import ContentAdd from 'material-ui/lib/svg-icons/content/add';
import NewRecordLabelSelect from './NewRecordLabelSelect';
import * as SubjectActions from '../../../../actions/subject';
import * as RecordActions from '../../../../actions/record';
import * as PDSActions from '../../../../actions/pds';

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

  renderRecords(recordNodes) {
    return (
      recordNodes ?
        <table className="table table-striped">
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
    const modalStyles = {
      width: '25%',
      height: '200px',
      position: 'fixed',
      top: '50%',
      left: '65%',
      marginTop: '-200px',
      marginLeft: '-25%',
      backgroundColor: '#fff',
      borderRadius: '15px',
      zIndex: 100,
      padding: '15px',
      boxShadow: '0 0 4px rgba(0,0,0,.14),0 4px 8px rgba(0,0,0,.28)',
    };
    const exRecStyle = {
      cursor: 'pointer',
      backgroundColor: '#ddecf9',
      borderTop: '1px solid #CCC5B9',
      borderBottom: '1px solid #CCC5B9',
    };

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
              style={exRecStyle}
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
            <FloatingActionButton
              onClick={() => this.handleNewRecordClick(this.props.pds)}
              backgroundColor={'#7AC29A'}
              mini
              style={addButtonStyle}
              disableTouchRipple={true}
            >
              <ContentAdd />
            </FloatingActionButton>
          :
            <FloatingActionButton
              disabled
              mini
              style={addButtonStyle}
            >
              <ContentAdd />
            </FloatingActionButton>}

        </h5>
        <div className="PDSRecords">
          {this.props.pds.authorized ?
            this.renderRecords(recordNodes)
            : <div> Not authorized for this Protocol Data Source </div>
          }
        </div>
        <hr />
      </div>
    );
  }
}

PDSRecordGroup.contextTypes = {
  history: React.PropTypes.object,
};

PDSRecordGroup.propTypes = {
  dispatch: React.PropTypes.func,
  protocol: React.PropTypes.object,
  pds: React.PropTypes.object,
  record: React.PropTypes.object,
  records: React.PropTypes.array,
  subject: React.PropTypes.object,
  activeRecord: React.PropTypes.object,
  activeLinks: React.PropTypes.array,
  linkMode: React.PropTypes.bool,
  selectedLabel: React.PropTypes.number,
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
