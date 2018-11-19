import React from 'react';
import PedigreeCardView from './PedigreeCardView';
import { connect } from 'react-redux';

// const SubjectPedigreePanel = (props) => {
//   return <SubjectPedigreeCardView />;
// };
//
// SubjectPedigreePanel.propTypes = {
//   edit: React.PropTypes.string,
//   path: React.PropTypes.string,
// };
class PedigreePanel extends React.Component {
  render() {
    return (<PedigreeCardView />);
  }
}

export default PedigreePanel;
// export default connect(SubjectPedigreePanel);
