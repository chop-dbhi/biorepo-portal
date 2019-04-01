// jscs:disable requireCamelCaseOrUpperCaseIdentifiers
// jscs:disable maximumLineLength
import React from 'react';
import { Link } from 'react-router';
import { connect } from 'react-redux';
import ExternalIDs from './ExternalIds';

const SubjectCardView = (props) => {
  const subject = props.subject.activeSubject;
  const editUrl = `${props.path}/edit`;
  return (
      <div className="card">
        <div className="more">
          <Link
            to={editUrl}
            type="button"
            style={{ marginRight: '40%' }}
            className="btn btn-simple btn-icon pull-right"
          >
            <i className="ti-pencil"></i>
          </Link>
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
  protocol: React.PropTypes.object,
  subject: React.PropTypes.object,
  pds: React.PropTypes.object,
  path: React.PropTypes.string,
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

export default connect(mapStateToProps)(SubjectCardView);
