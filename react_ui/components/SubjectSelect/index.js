import React from 'react';
import ReactTable from "react-table";
import { Link } from 'react-router-dom';
import 'react-table/react-table.css'
import Griddle, { pageProperties, plugins, RowDefinition, ColumnDefinition}from 'griddle-react';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';
import RaisedButton from '@material-ui/core/Button';
import BackButton from '../BackButton';
import NewSubjectForm from './NewSubjectForm';
import LoadingGif from '../LoadingGif';
import * as ProtocolActions from '../../actions/protocol';
import * as SubjectActions from '../../actions/subject';
import Button from 'react-bootstrap/Button'


class SubjectSelect extends React.PureComponent {

  constructor(props) {
    super(props);
    this.handleNewSubject = this.handleNewSubject.bind(this);
    this.handleClick = this.handleClick.bind(this);
    const { dispatch } = this.props;
  }

  componentDidMount() {
    const { dispatch } = this.props;
    this.props.dispatch(ProtocolActions.setActiveProtocol(this.props.match.params.id));
    this.props.dispatch(SubjectActions.fetchSubjects(this.props.match.params.id));

  }

  componentWillUnmount() {
    const { dispatch } = this.props;
    dispatch(SubjectActions.clearSubjectsState());
  }

  getActiveProtocol() {
    let activeProtocol = {};
    if (this.props.protocol.items) {
      activeProtocol = this.props.protocol;
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
    const subject = row.original;
    const { dispatch } = this.props;

    // Update state with new active subject
    dispatch(SubjectActions.setActiveSubject(subject));
    // Push to the correct pathname (and therefore view)
    this.props.history.push(`${this.props.match.url}/subject/${subject.id}`);
  }

  render() {
    // If this view is navigated to directly. Get active protocol based on param
    const subjects = this.props.subject.items;
    const protocol = this.getActiveProtocol();
    const filterCaseInsensitive = ({ id, value }, row) =>
      row[id] ? row[id].toLowerCase().includes(value.toLowerCase()) : true
    // const rows = this.griddleFrendlySubjects(); //This is not needed for react-table

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

    const columns = [{
      Header: 'Subjects',
      columns: [{
        Header: 'Organization',
        headerStyle: {textAlign: 'left'},
        accessor: 'organization_name', // String-based value accessors!
        style: { 'whiteSpace': 'unset' },
        Filter: ({filter, onChange}) => (<input placeholder="search" value={filter ? filter.value : ''}
                       onChange={event => onChange(event.target.value)} />),
        },
        {
        Header: 'Identifier',
        headerStyle: {textAlign: 'left'},
        accessor: 'organization_subject_id', // String-based value accessors!
        Filter: ({filter, onChange}) => (<input placeholder="search" value={filter ? filter.value : ''}
                       onChange={event => onChange(event.target.value)} />),
        },
        {
        Header: 'First Name',
        headerStyle: {textAlign: 'left'},
        accessor: 'first_name', // String-based value accessors!
        Filter: ({filter, onChange}) => (<input placeholder="search" value={filter ? filter.value : ''}
                       onChange={event => onChange(event.target.value)} />),
        },
        {
        Header: 'Last Name',
        headerStyle: {textAlign: 'left'},
        accessor: 'last_name', // String-based value accessors!
        Filter: ({filter, onChange}) => (<input placeholder="search" value={filter ? filter.value : ''}
                       onChange={event => onChange(event.target.value)} />),
        },
        {
        Header: 'Birth Date',
        headerStyle: {textAlign: 'left'},
        accessor: 'dob', // String-based value accessors!
        Filter: ({filter, onChange}) => (<input placeholder="search" value={filter ? filter.value : ''}
                       onChange={event => onChange(event.target.value)} />),
        }]
      }]


    return (
      this.props.subject.items.length>0 && this.props.protocol.items ?
        <div>
          {this.props.subject.addSubjectMode ?
            <NewSubjectForm orgs={this.props.protocol.orgs} /> :
            <div />
          }
          {!this.props.subject.addSubjectMode ?
            <BackButton /> :
            <div />
          }
          <h3>Project: {this.props.protocol.items.name}</h3>
          <div id="toolbar">
            <ul className="list-unstyled">
              <li>
                <Button
                  labelcolor={'#7AC29A'}
                  onClick={this.handleNewSubject}
                  label={'New Subject'}
                > New Subject </Button>
              </li>
            </ul>
          </div>
          <div style={subjectCountStyle}>{this.props.subject.items.length} Subjects</div>
          <div className="subject-table">
            {(this.props.subject.items.length>0) ?

              <ReactTable
                data={this.props.subject.items}
                columns={columns}
                filterable = {true}
                defaultFilterMethod={filterCaseInsensitive}
                className="-highlight"
                getTdProps={(state, rowInfo) => {
                  return {
                    onClick: (e, handleOrigional) => {
                      this.handleClick(rowInfo);
                    }
                  }}
                }
                />
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
