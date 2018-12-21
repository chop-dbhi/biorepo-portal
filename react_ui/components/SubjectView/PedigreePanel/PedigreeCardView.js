import React from 'react';
import { Link } from 'react-router';
import { connect } from 'react-redux';
import * as PedigreeActions from '../../../actions/pedigree';


class PedigreeCardView extends React.Component {

  constructor(props) {
    super(props);
  }
  componentWillUnmount() {
    const { dispatch } = this.props;
    dispatch(PedigreeActions.fetchPedigree(
      this.props.protocol.activeProtocolId,
      this.props.subject.id));
  }
  renderRelationships(relationships){
    return (
      recordNodes ?
        <table className="table table-striped">
          <thead>
            <tr><th>Relation</th><th>Record</th><th>Created</th><th>Modified</th></tr>
          </thead>
          <tbody>
            {relationships}
          </tbody>
        </table> : <div>No Relationships</div>
    );
  }

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
