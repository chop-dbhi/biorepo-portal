// jscs:disable requireCamelCaseOrUpperCaseIdentifiers
// jscs:disable maximumLineLength
import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import ExternalIDs from './ExternalIds';
import * as SubjectActions from '../../../actions/subject';
import { withRouter } from 'react-router';


function handleEditSubjectClick(props){
  const { dispatch } = props;
  dispatch(SubjectActions.setEditSubjectMode(true));
}

const SubjectCardView = (props) => {
  const subject = props.subject.activeSubject;
  const editUrl = `${props.path}/edit`;
  return (
        <div className="subject-card">
          <div class="row">
          <table className="table">
            <thead>
              <tr>
                <th><h4>Organization</h4></th>
                <th><h4>{subject.organization_id_label}</h4></th>
                <th><h4>First Name</h4></th>
                <th><h4>Last Name</h4></th>
                <th><h4>Date Of Birth</h4></th>
              </tr>
              <tr>

                <td><h5>{subject.organization_name}</h5></td>
                <td><h5>{subject.organization_subject_id}</h5></td>
                <td><b><h5>{subject.first_name}</h5></b></td>
                <td><b><h5>{subject.last_name}</h5></b></td>
                <td><h5>{subject.dob}</h5></td>
                <td><h5><i className="ti-pencil" onClick={() => handleEditSubjectClick(props)}></i></h5></td>
              </tr>

            </thead>
          </table>
          </div>
        </div>


  );
};

SubjectCardView.propTypes = {
  protocol: PropTypes.object,
  subject: PropTypes.object,
  pds: PropTypes.object,
  path: PropTypes.string,
  history: PropTypes.object,
};

function mapStateToProps(state) {
  return {
    protocol: {
      items: state.protocol.items,
    },
    subject: {
      items: state.subject.items,
      activeSubject: state.subject.activeSubject,
    },
    pds: {
      items: state.pds.items,
    },
  };
}

export default withRouter(connect(mapStateToProps)(SubjectCardView));
