import React from 'react';
import Griddle, { pageProperties, plugins, RowDefinition, ColumnDefinition}from 'griddle-react';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';
import RaisedButton from '@material-ui/core/Button';
import BackButton from '../BackButton';
import NewSubjectForm from './NewSubjectForm';
import LoadingGif from '../LoadingGif';
import * as ProtocolActions from '../../actions/protocol';
import * as SubjectActions from '../../actions/subject';

class SubjectSelect extends React.Component {

  constructor(props) {
    super(props);
    this.handleNewSubject = this.handleNewSubject.bind(this);
    this.handleClick = this.handleClick.bind(this);
    const { dispatch } = this.props;
  }

  componentDidMount() {
    const { dispatch } = this.props;
    this.props.dispatch(ProtocolActions.setActiveProtocol(this.props.match.params.id));
    // Check to see if subjects are loaded, if not fetch them
    if(this.props.subject.items.length == 0){
      this.props.dispatch(SubjectActions.fetchSubjects(this.props.match.params.id));
    }
  }

  getActiveProtocol() {
    let activeProtocol = {};
    if (this.props.protocol.items) {
      this.props.protocol.items.forEach((protocol) => {
        if (protocol.id === parseInt(this.props.protocol.activeProtocolId, 10)) {
          activeProtocol = protocol;
        }
      }, this);
    }
    return activeProtocol;
  }

  griddleFrendlySubjects() {
    let orgIdLabel = 'Identifier';
    let subs = [];
    let row = {};
    let rows = [];
    if (this.props.subject.items.length >0) {
      subs = this.props.subject.items.map((sub) => {
        let externalIds = '';
        sub.external_ids.forEach((exId) => {
          externalIds += `${exId.label_desc} : ${exId.record_id}\n`;
        }, this);
        let row = {
          Organization: sub.organization_name,
          'First Name': sub.first_name,
          'Last Name': sub.last_name,
          'Birth Date': sub.dob,
          'External IDs': externalIds,
          subject: sub,
        };
        row[orgIdLabel] = sub.organization_subject_id;
        // return row
        rows.push(row);
      });
    }
    return rows
  }

  handleNewSubject() {
    const { dispatch } = this.props;
    dispatch(SubjectActions.setAddSubjectMode(true));
    this.props.dispatch(ProtocolActions.setActiveProtocol(this.props.protocol.activeProtocolId));
  }

  handleClick(row) {
    const subject = row.props.data.subject;
    const { dispatch } = this.props;

    // Update state with new active subject
    dispatch(SubjectActions.setActiveSubject(subject));

    // Push to the correct pathname (and therefore view)
    this.props.history.push({
      pathname: `dataentry/protocol/${this.props.protocol.activeProtocolId}/subject/${subject.id}`,
    });
  }

  render() {
    // If this view is navigated to directly. Get active protocol based on param
    const subjects = this.props.subject.items;
    const protocol = this.getActiveProtocol();
    const rows = this.griddleFrendlySubjects();

    let manageExternalIDs = false;
    const subjectCountStyle = {
      paddingLeft: '10px',
      paddingRight: '10px',
      paddingBottom: '10px',
      color: '#7a7a7a',
      fontWeight: 'bold',
    };
    if (this.props.activeProtocolId) {
      if (parseInt(this.props.match.params.id, 10) === parseInt(protocol.id, 10)) {
        this.props.protocol.activeProtocol = protocol;
        protocol.data_sources.forEach((ds) => {
          // HACK obtains datasource Id
          const pdsId = parseInt(ds.slice(ds.length - 2, ds.length - 1), 10);
          if (pdsId === 3) {
            manageExternalIDs = true;
          }
        }, this);
      }
    }
    let orgIdLabel = 'Identifier';
    let columns = ['Organization', orgIdLabel, 'First Name', 'Last Name', 'Birth Date'];
    if (manageExternalIDs) {
      columns.push('External IDs');
    }

    return (
      this.props.protocol ?
        <div>
          {this.props.subject.addSubjectMode ?
            <NewSubjectForm orgs={this.props.protocol.orgs} /> :
            <div />
          }
          {!this.props.subject.addSubjectMode ?
            <BackButton /> :
            <div />
          }
          <h3>Project: {this.props.protocol.name}</h3>
          <div id="toolbar">
            <ul className="list-unstyled">
              <li>
                <RaisedButton
                  mini
                  labelcolor={'#7AC29A'}
                  onClick={this.handleNewSubject}
                  label={'New Subject'}
                />
              </li>
            </ul>
          </div>
          <div style={subjectCountStyle}>{this.props.subject.items.length} Subjects</div>
          <div className="subject-table">
            {(this.props.subject.items.length>0) ?
              <Griddle
                onRowClick={this.handleClick}
                data={rows}
                >
                pageProperties={{
                  currentPage: 1,
                  pageSize: 10,
                  recordCount: 10000,
                }}
                <RowDefinition>
                  <ColumnDefinition id="organization_name" title="Organization" />
                  <ColumnDefinition id="organization_subject_id" title="Identifier" />
                  <ColumnDefinition id="first_name" title="First Name" />
                  <ColumnDefinition id="last_name" title="Last Name" />
                  <ColumnDefinition id="dob" title="Birth Date" />
                </RowDefinition>
                </Griddle>
               : <LoadingGif />}
          </div>
        </div> :
        <div />
    );
  }
}

SubjectSelect.propTypes = {
  dispatch: PropTypes.func,
  history: PropTypes.object,
  params: PropTypes.object,
  subject: PropTypes.object,
  protocol: PropTypes.object,
};

function mapStateToProps(state) {
  return {
    protocol: {
      items: state.protocol.items,
      activeProtocolId: state.protocol.activeProtocolId,
      orgs: state.protocol.orgs,
      pds: state.pds,
    },
    subject: {
      items: state.subject.items,
      addSubjectMode: state.subject.addSubjectMode,
      isFetching: state.subject.isFetching,
    },
  };
}

export default connect(mapStateToProps)(SubjectSelect);
