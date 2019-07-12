// jscs:disable requireCamelCaseOrUpperCaseIdentifiers
import React from 'react';
import PropTypes from 'prop-types';
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
          <div>
            <div className="card">
              <PDSRecordGroup key={i} pds={_pds} records={pdsRecords} />
            </div>
            <hr/>
          </div>
        );
      }, this);
    }
    return (
      <div>
        <div className="content">
          {this.props.linkMode ? <LinkModeBanner /> : null}
          {this.props.selectLinkTypeModal ? <LinkRecord /> : null}
          {pdsNodes}
        </div>
        {this.props.activeLinks.length !== 0 && !this.props.isFetching ?
          <LinkedRecords /> : null
        }
      </div>
    );
  }
}

RecordPanel.propTypes = {
  dispatch: PropTypes.func,
  subject: PropTypes.object,
  protocol: PropTypes.object,
  pds: PropTypes.object,
  record: PropTypes.object,
  activeRecord: PropTypes.object,
  activeSubject: PropTypes.object,
  activeLinks: PropTypes.array,
  activeSubjectRecords: PropTypes.array,
  selectedLabel: PropTypes.number,
  linkMode: PropTypes.bool,
  selectLinkTypeModal: PropTypes.bool,
  isFetching: PropTypes.bool,
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
