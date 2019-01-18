import React from 'react';
import { Link } from 'react-router';
import { connect } from 'react-redux';
import * as PedigreeActions from '../../../actions/pedigree';


class PedigreeCardView extends React.Component {

  constructor(props) {
    super(props);
    this.state = { relationships: [],};
    console.log('we are in constructor')
  }
  componentDidMount() {
    console.log('we are in componentDidMount')
    const { dispatch } = this.props;

    dispatch(PedigreeActions.fetchPedigree(
      this.props.activeProtocolId,
      this.props.subject.id));
}
  render() {
    const protocol = this.props.activeProtocolId;
    const relationships = this.props.pedigree.items.items;
      if (relationships.length != 0){
        return (
          <div className="col-md-4 col-sm-6">
            <div className="card">
              <div className="content">
                <h5 className="category">Relationships</h5>
                <div className="more">
                  <i className="ti-pencil"></i>
                </div>
                <table className="table table-striped">
                  <thead>
                    <tr><th>Relation</th><th>MRN</th></tr>
                  </thead>

                  {relationships.relationships.map((relationship, i) => (
                      <thead><tr key={i}>
                        <th  > {relationship.subject_1_role} </th>
                        <th > {relationship.subject_1} </th></tr></thead>), this)}

                </table>
              </div>
            </div>
          </div>
        );
      }
      return(
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
      )
    }
  }

PedigreeCardView.propTypes = {
  dispatch: React.PropTypes.func,
  protocol: React.PropTypes.object,
  subject: React.PropTypes.object,
  activeRecord: React.PropTypes.object,
  activeProtocolId: React.PropTypes.number,
  pedigree: React.PropTypes.object,
  isFetching: React.PropTypes.bool,
};

function mapStateToProps(state) {
  return {
    pedigree: {
      isFetching: state.pedigree.isFetching,
      items: state.pedigree,
    },
    subject: state.subject.activeSubject,
    activeRecord: state.record.activeRecord,
    activeProtocol: state.protocol.activeProtocol,
    activeProtocolId: state.protocol.activeProtocolId,
  };
}

export default connect(mapStateToProps)(PedigreeCardView);
