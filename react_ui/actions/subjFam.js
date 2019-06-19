
import fetch from 'isomorphic-fetch';
import * as NotificationActions from './notification';

export const REQUEST_SUBJ_FAM = 'REQUEST_SUBJ_FAM';
export const RECEIVE_SUBJ_FAM = 'RECEIVE_SUBJ_FAM';
export const SET_ACTIVE_SUBJ_FAM_REL = 'SET_ACTIVE_SUBJ_FAM_REL';
export const ADD_SUBJ_FAM_REL_SUCCESS = 'ADD_SUBJ_FAM_REL_SUCCESS';
export const ADD_SUBJ_FAM_REL_REQUEST = 'ADD_SUBJ_FAM_REL_REQUEST';
export const ADD_SUBJ_FAM_REL_FAILURE = 'ADD_SUBJ_FAM_REL_FAILURE';
export const SET_ADD_SUBJ_FAM_REL_MODE = 'SET_ADD_SUBJ_FAM_REL_MODE';
export const CLEAR_SUBJ_FAM_STATE = 'CLEAR_SUBJ_FAM_STATE';
export const SET_UPDATE_FORM_ERRORS = 'SET_UPDATE_FORM_ERRORS';
export const REQUEST_RELATIONSHIP_TYPES = 'REQUEST_RELATIONSHIP_TYPES';
export const RECEIVE_RELATIONSHIP_TYPES = 'RECEIVE_RELATIONSHIP_TYPES';


function checkResponse(response) {
  if (response.status >= 200 && response.status < 300) {
    return response;
  }
  const error = new Error(response.statusText);
  error.response = response;
  throw error;
}

export function requestSubjFam() {
  return {
    type: REQUEST_SUBJ_FAM,
  };
}

export function receiveSubjFam(json) {
    return{
      type: RECEIVE_SUBJ_FAM,
      subjFam: json,
    };
  }

export function requestRelTypes() {
  return{
    type: REQUEST_RELATIONSHIP_TYPES,
  };
}

export function receiveRelTypes(json) {
  return {
    type: RECEIVE_RELATIONSHIP_TYPES,
    relTypes: json,
  };
}

export function fetchRelationshipTypes() {
  const url = `api/subj_fam/relationship_types`;
  return dispatch => {
    dispatch(requestRelTypes());
    return fetch(url, {
      method: 'GET',
      headers: {
        Accept: 'application/json',
        Authorization: `token ${token}`,
      },
    })
    .then(checkResponse)
    .then(response => response.json())
    .then(json => dispatch(receiveRelTypes(json)));
  };
}

export function fetchSubjFam(protocolID, subjectId) {
  const url = `api/protocols/${protocolID}/subj_fam/subject/${subjectId}`;
  return dispatch => {
    dispatch(requestSubjFam());
    return fetch(url, {
      method: 'GET',
      headers: {
        Accept: 'application/json',
        Authorization: `token ${token}`,
      },
    })

  // };
      .then(checkResponse)
      .then(response => response.json())
      .then(json => dispatch(receiveSubjFam(json)));
    //   .catch(error => {
    //     dispatch(NotificationActions.addNotification(
    //       {
    //         message: 'Error Contacting the electronic Honest Broker',
    //         level: 'error',
    //         error,
    //       }
    //     ));
    //
    //     // This is a bit of a hack to get the Notification System to render properly.
    //     dispatch(NotificationActions.renderNotification());
    //   }
    // );
  };
}
export function clearSubjFamState() {
  return {
    type: CLEAR_SUBJ_FAM_STATE,
  };
}

export function checkAddSubjFamRel(json) {
  const [success, relationship, errors] = json;
  if (success) {
    return relationship;
  }
  const error = new Error('Unable to add relationship');
  error.errors = errors;
  throw error;
}

export function setAddSubjFamRelMode(mode = null) {
  // Update state to enable or disable Addrelationship mode
  return {
    type: SET_ADD_SUBJ_FAM_REL_MODE,
    mode,
  };
}

export function addSubjFamRelRequest() {
  return {
    type: ADD_SUBJ_FAM_REL_REQUEST,
  };
}

export function addSubjFamRelSuccess(subjFamRel) {
  return dispatch => {
    // dispatch(NotificationActions.addNotification(
    //   {
    //     message: 'Relationship Added',
    //     level: 'success',
    //     autoDismiss: 2,
    //   }
    // ));
    dispatch(setAddSubjFamRelMode());
    dispatch({
      type: ADD_SUBJ_FAM_REL_SUCCESS,
      isSaving: false,
      subjFamRel,
    })
    dispatch(fetchSubjFam(subjFamRel.protocol_id, subjFamRel.subject_1))
  };
}

export function addSubjFamRelFailure(error) {
  const errors = error.errors;
  return {
    type: ADD_SUBJ_FAM_REL_FAILURE,
    errors,
  };
}
export function setUpdateFormErrors(error) {
  return {
    type: SET_UPDATE_FORM_ERRORS,
    error,
  };
}

//add subjFam relationship to the eHB
export function addSubjFamRel(protocolId, subjFamRel) {
  return dispatch => {
    dispatch(addSubjFamRelRequest());
    const url = `api/protocols/${protocolId}/subj_fam/create/`;
    return fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `token ${token}`,
        'X-CSRFToken': csrf_token,
      },
      body: JSON.stringify(subjFamRel),
    })
      .then(response => response.json())
      .then(checkAddSubjFamRel)
      .then(subjFamRel => dispatch(addSubjFamRelSuccess(subjFamRel)))
      .then(dispatch(fetchSubjFam(protocolId, subjFamRel.subject_1)))
  };
}

export function setActiveSubjFamRel(subjFam) {
  return {
    type: SET_ACTIVE_SUBJ_FAM_REL,
    activeSubjFam: subjFam,
  };
}
