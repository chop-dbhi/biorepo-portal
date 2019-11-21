import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import * as SubjFamActions from '../../../actions/subjFam';
import { withStyles } from '@material-ui/core/styles';
import Icon from '@material-ui/core/Icon';
import FloatingActionButton from '@material-ui/core/Button';
import AddButton from '../../addButton'

class SubjFamCardView extends React.Component {

  constructor(props) {
    super(props);
    this.handleNewSubjFamRelClick = this.handleNewSubjFamRelClick.bind(this);
    this.handelRelClick = this.handleRelClick.bind(this);
    this.handleDeleteSubjRel = this.handleDeleteSubjRel.bind(this);
  }

  // get the related subject and the related
  // subject role in json format by filtering out current subject info.
  organizeRelationshipList() {
    const relationships = this.props.subjFam.items.items;
    const subject = this.props.subject;
    const organizedRelationships = [];

    // return null if there are no relationships in the eHB
    if (relationships){
      relationships.relationships.forEach(function (relationship) {
        if (relationship.subject_1_id == subject.id) {
          organizedRelationships.push({ "subject_org_id": relationship.subject_1_org_id,
                                      "subject_role": relationship.subject_1_role,
                                      "subject_id": relationship.subject_1_id,
                                      "id": relationship.id,
                                      "related_subject_role": relationship.subject_2_role,
                                      "related_subject_org_id": relationship.subject_2_org_id,
                                      "related_subject_id": relationship.subject_2_id,
                                      "current_subject": 1});
        }
        else {
          organizedRelationships.push({"subject_org_id": relationship.subject_2_org_id,
                                      "subject_role": relationship.subject_2_role,
                                      "subject_id": relationship.subject_2_id,
                                      "id": relationship.id,
                                      "related_subject_role": relationship.subject_1_role,
                                      "related_subject_org_id": relationship.subject_1_org_id,
                                      "related_subject_id": relationship.subject_1_id,
                                      "current_subject": 2});
        }
      });
    }
    // return null if there are no relationships in the eHB
    if (organizedRelationships.length == 0){
      return null;
    }
    else{
      return organizedRelationships
    }
  }

  renderRelationships(relationships){
    return(
      relationships ?
        relationships.map((item, i)=> (
          <tr
            key={i}
            className="ExternalRecord"
          >
            <td onClick={() => this.handleRelClick(item.related_subject_id)}>
              {item.related_subject_role}
            </td>
            <td onClick={() => this.handleRelClick(item.related_subject_id)}>
              {item.related_subject_org_id}
            </td>
            <td onClick={() => this.handleEditSubjFamRelClick(item)}>
              <i className="ti-pencil" ></i>
            </td>
            <td onClick={() => this.handleDeleteSubjRel(item)}> <i className="ti-trash" ></i> </td>
          </tr>))
          :
          <tr>
            <td> No Relationships </td>
            <td>  </td>
          </tr>
    );
  }

  handleNewSubjFamRelClick(subj_fam_relationship) {
    const { dispatch } = this.props;
    dispatch(SubjFamActions.setActiveSubjFamRel(subj_fam_relationship));
    dispatch(SubjFamActions.setAddSubjFamRelMode(true));
  }

  handleEditSubjFamRelClick(subj_fam_relationship) {
    const { dispatch } = this.props;
    dispatch(SubjFamActions.setActiveSubjFamRel(subj_fam_relationship));
    dispatch(SubjFamActions.setEditSubjFamRelMode(true));
  }

  handleDeleteSubjRel(subj_fam_relationship){
    const { dispatch } = this.props;
    dispatch(SubjFamActions.setActiveSubjFamRel(subj_fam_relationship));
    dispatch(SubjFamActions.setDeleteSubjFamRelMode(true));
  }

  handleRelClick(subjectId){
    const url = `#/dataentry/protocol/${this.props.activeProtocolId}/subject/${subjectId}`;
    window.location.href = url;
    window.location.reload();
  }

  render() {
    const protocol = this.props.activeProtocolId;
    const relationships = this.props.subjFam.items.items;
    let organizedRelationships = null;
    if (relationships.length !=0){
      organizedRelationships = this.organizeRelationshipList();
      }
    else {
      organizedRelationships = null;
    }
    return (
      <div className="relationship-card">
        <div className="content">
          <h5 className="category"> Relationships
          <div  onClick={() => this.handleNewSubjFamRelClick(this.props.subjFam)}>
            <AddButton/>
          </div>
          </h5>
          <table className="table">
            <thead>
              <tr><th>Relation</th><th>MRN</th></tr>
            </thead>
            <tbody>
              {this.renderRelationships(organizedRelationships)}
            </tbody>
          </table>
        </div>
      </div>
    );
  }
}

SubjFamCardView.propTypes = {
  dispatch: PropTypes.func,
  protocol: PropTypes.object,
  subject: PropTypes.object,
  activeRecord: PropTypes.object,
  activeProtocolId: PropTypes.number,
  subjFam: PropTypes.object,
  isFetching: PropTypes.bool,
  activeSubjFam: PropTypes.object,
};

function mapStateToProps(state) {
  return {
    subjFam: {
      isFetching: state.subjFam.isFetching,
      items: state.subjFam,
    },
    subject: state.subject.activeSubject,
    activeRecord: state.record.activeRecord,
    activeProtocol: state.protocol.activeProtocol,
    activeProtocolId: state.protocol.activeProtocolId,
    activeSubjFam: state.subjFam.activeSubjFam,
  };
}

export default connect(mapStateToProps)(SubjFamCardView);
