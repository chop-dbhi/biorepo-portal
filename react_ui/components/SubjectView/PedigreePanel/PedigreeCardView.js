import React from 'react';
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
    console.log('this.props.pedigree.items')
    console.log(this.props.pedigree.items.items)
    const protocol = this.props.activeProtocolId;
    const relationships = this.props.pedigree.items.items;
    // if (this.props.pedigree.items == null){
    //   const relationships = [];
    // } else {
    //   const relationships = this.props.pedigree.items;
    // }
    // const { relationships } = this.state;
    console.log('this.state')
    console.log(this.state)

    // relationships = PedigreeActions.fetchPedigree(
    //                         protocol,
    //                         this.props.subject.id);
    console.log('this.state.pedigree')
    console.log(this.props.pedigree)
    // const relationships = this.state.relationships;
    console.log('relationships')
    console.log( relationships )
    // if (this.props.pedigree.items) {
    //   this.props.pedigree.items.map((relationship, i) => {
    //     console.log('relationship subject_1')
    //     console.log(this.props.pedigree.items.subject_1)

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
  // },this);

//   <div className="col-md-4 col-sm-6">
//     <div className="card">
//       <div className="more">
//         <i className="ti-pencil"></i>
//       </div>
//       <div className="content">
//         <h4 className="title">Relationships</h4>
//         <p className="description">Mother</p>
//         <p className="description">Father</p>
//       </div>
//     </div>
//   </div>
// );
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


PedigreeCardView.propTypes = {
  dispatch: React.PropTypes.func,
  protocol: React.PropTypes.object,
  subject: React.PropTypes.object,
  activeRecord: React.PropTypes.object,
  activeProtocolId: React.PropTypes.number,
  pedigree: React.PropTypes.object,
  isFetching: React.PropTypes.bool,
};
// function mapDispatchToProps (dispatch) {
//   return {
//     pedigree: () => dispatch(PedigreeActions.fetchPedigree(
//       this.props.activeProtocolId,
//       this.props.subject.id))
//   }
// }
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
// export default connect(mapStateToProps);
export default connect(mapStateToProps)(PedigreeCardView);
