// jscs:disable requireCamelCaseOrUpperCaseIdentifiers
import React from 'react';
import PropTypes from 'prop-types';

const ExternalIDs = (props) => {
  let nodes = null;
  if (props.externalIds) {
    nodes = props.externalIds.map((id, i) => (
      <li key={i}>{id.label_desc}: {id.record_id}</li>
    ), this);
  }
  const idList = (
    <ul className="externalIds">
      {nodes}
    </ul>
  );
  return (
    <div>
      <h6 className="category">External Identifiers</h6>
      {idList}
    </div>
  );
};

ExternalIDs.propTypes = {
  externalIds: PropTypes.array,
};

export default ExternalIDs;
