// Helper functions used by muliple components

//imports for SubjectFamPanel
import * as SubjFamActions from '../actions/subjFam';

// SubjectFamPanel Helper Functions
export function organizeSubjFamRelForEdit(){
  const { dispatch } = this.props;
  let subject_role = null
  let related_subject_role = null
  let related_subject = null

  if (this.props.editSubjFamRelMode){
    subject_role = this.state.subjectRole.label;
    related_subject_role = this.state.relatedSubjectRole.label;
    related_subject = this.state.relatedSubject.value;
  }
  else if (this.props.deleteSubjFamRelMode) {
    subject_role = this.state.subjectRole;
    related_subject_role = this.state.relatedSubjectRole;
    related_subject = this.state.relatedSubjectId;
  }
  else {
    subject_role = this.state.subjectRole.value;
    related_subject_role = this.state.relatedSubjectRole.value;
    related_subject = this.state.relatedSubject.value;
  }

  if (this.props.activeSubjFam.current_subject == 1) {
    var updatedRel = {
        "subject_1": this.props.subject.activeSubject.id,
        "subject_2": related_subject,
        "subject_1_role": (((this.state.subjectRole.value != null) && (this.state.subjectRole.value != undefined)) ? this.state.subjectRole.value
                          : getRelTypeValue(subject_role, this.props.relTypes[0])),
        "subject_2_role": ((this.state.relatedSubjectRole.value != null) ? this.state.relatedSubjectRole.value
                          : getRelTypeValue(related_subject_role, this.props.relTypes[0])),
        "protocol_id": this.props.protocol.activeProtocolId,
        "id": this.props.activeSubjFam.id,
    }
  }
  else {
    var updatedRel = {
        "subject_1": related_subject,
        "subject_2": this.props.subject.activeSubject.id,
        "subject_1_role": ((this.state.relatedSubjectRole.value != null) ? this.state.relatedSubjectRole.value
                          :(getRelTypeValue(related_subject_role, this.props.relTypes[0]))),
        "subject_2_role": ((this.state.subjectRole.value != null) ? this.state.subjectRole.value
                          :getRelTypeValue(subject_role, this.props.relTypes[0])),
        "protocol_id": this.props.protocol.activeProtocolId,
        "id": this.props.activeSubjFam.id,
    }
  }
  return updatedRel;
}

export function handleRelEditDelCloseClick() {
  const { dispatch } = this.props;
  dispatch(SubjFamActions.setAddSubjFamRelMode(false));
  dispatch(SubjFamActions.setEditSubjFamRelMode(false));
  dispatch(SubjFamActions.setDeleteSubjFamRelMode(false));
}

export function getRelTypeValue(relTypeDesc, relTypes) {
    let relTypeValue = null;
    relTypes.forEach(function (relType) {
        if (relType.desc == relTypeDesc) {
          relTypeValue = relType.id
        }
    });
    return relTypeValue;
  }
