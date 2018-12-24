// jscs:disable requireCamelCaseOrUpperCaseIdentifiers
import React from 'react';
import PDSRecordGroup from './PDSRecordGroup';
import LinkModeBanner from '../Modals/LinkModeBanner';
import LinkRecord from '../Modals/LinkRecord';
import LinkedRecords from './LinkedRecords';
import * as SubjectActions from '../../../actions/subject';
import { connect } from 'react-redux';

class RecordPanel extends React.Component {

  componentDidMount() {
    const { dispatch } = this.props;
    dispatch(SubjectActions.setActiveSubject(this.props.subject));
  }

  render() {
    const pds = this.props.pds;
    const records = this.props.record.items;
    let pdsNodes = null;
    if (pds.items) {
      pdsNodes = pds.items.map((_pds, i) => {
        const pdsRecords = records.filter((record) => {
          if (_pds.id === record.pds) {
            return record;
          }
          return null;
        });
        return (
          <PDSRecordGroup key={i} pds={_pds} records={pdsRecords} />
        );
      }, this);
    }
    return (
      <div>
          <div className="card">
            <div className="content">
              {this.props.linkMode ? <LinkModeBanner /> : null}
              {this.props.selectLinkTypeModal ? <LinkRecord /> : null}
              {pdsNodes}
            </div>
          </div>
        {this.props.activeLinks.length !== 0 && !this.props.isFetching ?
          <LinkedRecords /> : null
        }
      </div>
    );
  }
}

RecordPanel.propTypes = {
  dispatch: React.PropTypes.func,
  subject: React.PropTypes.object,
  protocol: React.PropTypes.object,
  pds: React.PropTypes.object,
  record: React.PropTypes.object,
  activeRecord: React.PropTypes.object,
  activeSubject: React.PropTypes.object,
  activeLinks: React.PropTypes.array,
  activeSubjectRecords: React.PropTypes.array,
  selectedLabel: React.PropTypes.number,
  linkMode: React.PropTypes.bool,
  selectLinkTypeModal: React.PropTypes.bool,
  isFetching: React.PropTypes.bool,
};

function mapStateToProps(state) {
  return {
    protocol: {
      items: state.protocol.items,
      activeProtocol: state.protocol.activeProtocol,
    },
    pds: {
      items: state.pds.items,
    },
    record: {
      items: state.record.items,
    },
    activeRecord: state.record.activeRecord,
    activeSubject: state.subject.activeSubject,
    activeLinks: state.record.activeLinks,
    activeSubjectRecords: state.subject.activeSubjectRecords,
    selectedLabel: state.record.selectedLabel,
    linkMode: state.subject.linkMode,
    selectLinkTypeModal: state.record.selectLinkTypeModal,
    isFetching: state.record.isFetching,
  };
}

export default connect(mapStateToProps)(RecordPanel);
