import React from 'react';
import { Link } from 'react-router';
import { connect } from 'react-redux';

// const SubjectPedigreeCardView = (props) => {
class PedigreeCardView extends React.Component {
  // const subject = props.subject.activeSubject;
  render() {
    return (
      <div className="col-md-4 col-sm-6">
        <div className="card">
          <div className="more">
              <i className="ti-pencil"></i>
          </div>
          <div className="content">
            <h4 className="title">Relationships</h4>
            <p className="description">Mother</p>
            <p className="description">Father</p>
          </div>
        </div>
      </div>
    );
  }
}

// export default connect(SubjectPedigreeCardView);
export default PedigreeCardView;
