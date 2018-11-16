import React from 'react';
import SubjectPedigreeCardView from './SubjectPedigreeCardView';
import { connect } from 'react-redux';

// const SubjectPedigreePanel = (props) => {
//   return <SubjectPedigreeCardView />;
// };
//
// SubjectPedigreePanel.propTypes = {
//   edit: React.PropTypes.string,
//   path: React.PropTypes.string,
// };
class SubjectPedigreePanel extends React.Component {
  render() {
    return (<SubjectPedigreeCardView />);
  }
}

export default SubjectPedigreePanel;
// export default connect(SubjectPedigreePanel);
