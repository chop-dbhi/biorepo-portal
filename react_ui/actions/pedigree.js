
import fetch from 'isomorphic-fetch';

export const REQUEST_PEDIGREE = 'REQUEST_PEDIGREE';
export const RECEIVE_PEDIGREE = 'RECEIVE_PEDIGREE';
export const SET_ACTIVE_PEDIGREE = 'SET_ACTIVE_PEDIGREE';
export const ADD_PEDIGREE_REL_SUCCESS = 'ADD_PEDIGREE_REL_SUCCESS';
export const ADD_PEDIGREE_REL_REQUEST = 'ADD_PEDIGREE_REL_REQUEST';
export const ADD_PEDIGREE_REL_FAILURE = 'ADD_PEDIGREE_REL_FAILURE';
export const SET_ADD_PEDIGREE_REL_MODE = 'SET_ADD_PEDIGREE_REL_MODE';

function checkResponse(response) {
  if (response.status >= 200 && response.status < 300) {
    return response;
  }
  const error = new Error(response.statusText);
  error.response = response;
  throw error;
}

export function requestPedigree() {
  return {
    type: REQUEST_PEDIGREE,
  };
}

export function receivePedigree(json) {
    return{
      type: RECEIVE_PEDIGREE,
      pedigree: json,
    };
  }

export function fetchPedigree(protocolID, subjectId) {
  const url = `api/protocols/${protocolID}/pedigree/subject/${subjectId}`;
  return dispatch => {
    dispatch(requestPedigree());
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
      .then(json => dispatch(receivePedigree(json)));
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

export function checkAddPedigreeRel(json) {
  const [success, relationship, errors] = json;
  if (success) {
    return relationship;
  }
  const error = new Error('Unable to add subject');
  error.errors = errors;
  throw error;
}

export function setAddPedigreeRelMode(mode = null) {
  // Update state to enable or disable AddSubject mode
  return {
    type: SET_ADD_PEDIGREE_REL_MODE,
    mode,
  };
}

export function addPedigreeRelRequest() {
  return {
    type: ADD_PEDIGREE_REL_REQUEST,
  };
}

export function addPedigreeRelSuccess(pedigreeRel) {
  return dispatch => {
    dispatch(NotificationActions.addNotification(
      {
        message: 'Relationship Added',
        level: 'success',
        autoDismiss: 2,
      }
    ));
    dispatch(setAddPedigreeRelMode());
    dispatch({
      type: ADD_PEDIGREE_REL_SUCCESS,
      isSaving: false,
      pedigreeRel,
    });
  };
}

export function addPedigreeRelFailure(error) {
  const errors = error.errors;
  return {
    type: ADD_PEDIGREE_REL_FAILURE,
    errors,
  };
}

// TODO: add pedigree relationship to the eHB
export function addPedigreeRel(protocolId, pedigreeRel) {
  return dispatch => {
    dispatch(addPedigreeRelRequest());
    const url = `api/protocols/${protocolId}/subjects/create`;
    return fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Accept: 'application/json',
        Authorization: `token ${token}`,
        'X-CSRFToken': csrf_token,
      },
      body: JSON.stringify(pedigreeRel),
    })
      .then(response => response.json())
      .then(checkAddPedigreeRel)
      .then(pedigreeRel => dispatch(addPedigreeRelSuccess(pedigreeRel)))
      .catch(errors => dispatch(addPedigreeRelFailure(errors)));
  };
}

export function setActivePedigree(pedigree) {
  return {
    type: SET_ACTIVE_PEDIGREE,
    activePedigree: pedigree,
  };
}
