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
      relationships ?
        <table className="table table-striped">
          <thead>
            <tr><th>Relation</th><th>Organization ID</th></tr>
          </thead>
          <tbody>
            {relationships}
          </tbody>
        </table> : <div>No Relationships</div>
    );
  }

  render() {
    relationships = PedigreeActions.fetchPedigree(
                            this.props.protocol.activeProtocolId,
                            this.props.subject.id);
    if (relationships.length !== 0) {
      relationships = relationships.map((relationships, i) => {
        let linkIcon = null;
        // TODO: Factor out these record lines into their own components.
        if (this.props.activePedigree != null && (this.props.activePedigree.id === relationship.id)) {
          return (
            // TODO: add onclick function to add ability to edit/add a pedigree relationship
            <tr>
              <td>{relationship.id}</td>
              <td>{relationship.subject_1_role}</td>
            </tr>
          );
        }


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
          <tr>
            <td>{relationship.id}</td>
            <td>{linkIcon} {relationship.subject_1_role}</td>
          </tr>
        </div>
      </div>
    );
  }, this);
  }
  }
}

function mapStateToProps(state) {
  return {
    relationships: {
      isFetching: state.record.isFetching,
    },
    subject: state.subject.activeSubject,
    activeRecord: state.record.activeRecord,
    };
  }
// export default connect(SubjectPedigreeCardView);
export default connect(mapStateToProps)(PedigreeCardView);
