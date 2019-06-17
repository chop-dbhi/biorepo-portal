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
      <div className="card">
        <div className="more">
            <i className="ti-pencil" onClick={() => handleEditSubjectClick(props)}></i>
        </div>
        <div className="content">
          <h6 className="category">{subject.organization_name}</h6>
          <h4 className="title">{subject.first_name} {subject.last_name}</h4>
          <p className="description">{subject.organization_id_label}: {subject.organization_subject_id}</p>
          <p className="description">Date of birth: {subject.dob}</p>
          <ExternalIDs externalIds={subject.external_ids} />
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
