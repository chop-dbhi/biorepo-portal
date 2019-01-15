import React, {PropTypes} from 'react';
// import PropTypes from 'prop-types'
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
      // .then(results => {
      //     console.log(results)
      //     // return results.json();
      //     return results;
      //   }).then(data => {
      //     // let this.state.relationships = data.results
      //     console.log('data')
      //     console.log(data)
      //     this.setState({relationships: data})

    // console.log(this.props.activeProtocolId)
    // console.log('Subject ID')
    // console.log(this.props.subject.id)
    // console.log('fetch in Component did mount')
    // console.log(fetch(PedigreeActions.fetchPedigree(
    //   this.props.activeProtocolId,
    //   this.props.subject.id)))
    // dispatch(PedigreeActions.fetchPedigree(
    //   this.props.activeProtocolId,
    //   this.props.subject.id))
    //   .then(results => {
    //     console.log(results)
    //     // return results.json();
    //     return results;
    //   }).then(data => {
    //     // let this.state.relationships = data.results
    //     console.log('data')
    //     console.log(data)
    //     this.setState({relationships: data})
    //   })

      // this.setState({relationships: relationships});

  // })
}

  // renderRelationships(relationships){
  //   return (
  //     relationships ?
  //       <table className="table table-striped">
  //         <thead>
  //           <tr><th>Relation</th><th>Organization ID</th></tr>
  //         </thead>
  //         <tbody>
  //           {this.state.relationships}
  //         </tbody>
  //       </table> : <tr>No Relationships</tr>
  //   );
  // }

  render() {
    console.log('we are in render')
    const protocol = this.props.activeProtocolId;
    // const { relationships } = this.state;
    console.log('this.state')
    console.log(this.state)

    // relationships = PedigreeActions.fetchPedigree(
    //                         protocol,
    //                         this.props.subject.id);
    console.log('this.props.pedigree')
    console.log(this.props.pedigree)
    const relationships = this.state.relationships;
    console.log('relationships')
    console.log(relationships)
    if (this.props.pedigree != []) {
      this.state.relationships.map((relationship, i) => {
        console.log('relationship subject_1')
        console.log(this.state.relationship.subject_1)
        // let linkIcon = null;
        // TODO: Factor out these record lines into their own components.
        // if (this.props.activePedigree != null && (this.props.activePedigree.id === relationship.id)) {
        //   return (
        //     // TODO: add onclick function to add ability to edit/add a pedigree relationship
        //     <tr>
        //       <td>{relationship.id}</td>
        //       <td>{relationship.subject_1_role}</td>
        //     </tr>
        //   );
        // }
// }

      return (
        <div className="col-md-4 col-sm-6">
          <div className="card">
            <div className="more">
                <i className="ti-pencil"></i>
            </div>
            <table className="table table-striped">
              <thead>
                <tr><th>Relation</th><th>Organization ID</th></tr>
              </thead>
              <tbody>
                {this.state.relationship.subject_1}
              </tbody>
            </table>
          </div>
        </div>
      );
  });
} else { return (
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
    // return (
    //   <div className="col-md-4 col-sm-6">
    //     <div className="card">
    //       <div className="more">
    //           <i className="ti-pencil"></i>
    //       </div>
    //       <div className="content">
    //         <h4 className="title">Relationships</h4>
    //         <p className="description">Mother</p>
    //         <p className="description">Father</p>
    //       </div>
    //     </div>
    //   </div>
    // )
  }
  }
}

PedigreeCardView.propTypes = {
  protocol: React.PropTypes.object,
  subject: React.PropTypes.object,
  activeRecord: React.PropTypes.object,
  activeProtocolId: React.PropTypes.number,
  pedigree: React.PropTypes.object,
  // isFetching: React.PropTypes.bool,
};

function mapStateToProps(state) {
  return {
    // pedigree: state.pedigree.activePedigree,
    //   // isFetching: state.relationships.isFetching,
    //   pedigree: state.relationships.pedigree,
    // },
    subject: state.subject.activeSubject,
    activeRecord: state.record.activeRecord,
    activeProtocol: state.protocol.activeProtocol,
    activeProtocolId: state.protocol.activeProtocolId,
  };
}
// export default connect(mapStateToProps);
export default connect(mapStateToProps)(PedigreeCardView);
