import React from 'react';
import PropTypes from 'prop-types';
import SubjectCardEdit from './SubjectCardEdit';
import SubjectCardView from './SubjectCardView';

const SubjectPanel = (props) => {
  const path = props.path;
  if (props.edit) {
    return <SubjectCardEdit path={path} />;
  }
  return <SubjectCardView path={path} />;
};

SubjectPanel.propTypes = {
  edit: PropTypes.string,
  path: PropTypes.string,
};
export default SubjectPanel;
