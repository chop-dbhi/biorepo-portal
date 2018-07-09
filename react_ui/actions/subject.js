/* global token csrf_token*/
import fetch from 'isomorphic-fetch';
import * as RecordActions from './record';
import * as NotificationActions from './notification';
export const REQUEST_SUBJECTS = 'REQUEST_SUBJECTS';
export const RECEIVE_SUBJECTS = 'RECEIVE_SUBJECTS';
export const REQUEST_SUBJECT = 'REQUEST_SUBJECT';
export const RECEIVE_SUBJECT = 'RECEIVE_SUBJECT';
export const REQUEST_SUBJECT_SUCCESS = 'REQUEST_SUBJECT_SUCCESS';
export const SET_ACTIVE_SUBJECT = 'SET_ACTIVE_SUBJECT';
export const UPDATE_SUBJECT_REQUEST = 'UPDATE_SUBJECT_REQUEST';
export const UPDATE_SUBJECT_FAILURE = 'UPDATE_SUBJECT_FAILURE';
export const UPDATE_SUBJECT_SUCCESS = 'UPDATE_SUBJECT_SUCCESS';
export const ADD_SUBJECT_REQUEST = 'ADD_SUBJECT_REQUEST';
export const ADD_SUBJECT_FAILURE = 'ADD_SUBJECT_FAILURE';
export const ADD_SUBJECT_SUCCESS = 'ADD_SUBJECT_SUCCESS';
export const SET_LINK_MODE = 'SET_LINK_MODE';
export const SET_ADD_SUBJECT_MODE = 'SET_ADD_SUBJECT_MODE';
export const SET_NEW_SUBJECT = 'SET_NEW_SUBJECT';
export const REQUEST_SUBJECT_RECORDS = 'REQUEST_SUBJECT_RECORDS';
export const RECEIVE_SUBJECT_RECORDS = 'RECEIVE_SUBJECT_RECORDS';
export const SET_NEW_SUBJECT_FORM_ERRORS = 'SET_NEW_SUBJECT_FORM_ERRORS';
export const SET_UPDATE_FORM_ERRORS = 'SET_UPDATE_FORM_ERRORS';

function checkStatus(response) {
  if (response.status >= 200 && response.status < 300) {
    return response;
  }
  const error = new Error(response.statusText);
  error.response = response;
  return error;
}

function checkAddSubject(json) {
  const [success, subject, errors] = json;
  if (success) {
    return subject;
  }
  const error = new Error('Unable to add subject');
  error.errors = errors;
  throw error;
}

export function requestSubjects() {
  return {
    type: REQUEST_SUBJECTS,
    subjects: [],
    isFetching: true,
  };
}

export function receiveSubjects(json) {
  return {
    type: RECEIVE_SUBJECTS,
    subjects: json,
    isFetching: false,
    receivedAt: Date.now(),
  };
}

export function requestSubject() {
  return {
    type: REQUEST_SUBJECT,
  };
}

export function receiveSubject(json) {
  return {
    type: REQUEST_SUBJECT_SUCCESS,
    subject: json,
  };
}

export function setAddSubjectMode(mode = null) {
  // Update state to enable or disable AddSubject mode
  return {
    type: SET_ADD_SUBJECT_MODE,
    mode,
  };
}

export function setActiveSubject(subject) {
  return dispatch => {
    dispatch(RecordActions.setActiveRecord(null));
    dispatch({
      type: SET_ACTIVE_SUBJECT,
      subject,
    });
  };
}

export function setNewSubject(subject) {
  return {
    type: SET_NEW_SUBJECT,
    subject,
  };
}

export function fetchSubjects(protocolId) {
  return dispatch => {
    dispatch(requestSubjects(protocolId));
    const url = `api/protocols/${protocolId}/subjects/`;
    return fetch(url, {
      method: 'GET',
      headers: {
        Accept: 'application/json',
        Authorization: `token ${token}`,
      },
    })
      .then(response => response.json())
      .then(json => dispatch(receiveSubjects(json)));
  };
}

export function fetchSubject(protocolId, subjectId) {
  return dispatch => {
    dispatch(requestSubject());
    const url = `api/protocols/${protocolId}/subjects/${subjectId}`;
    return fetch(url, {
      method: 'GET',
      headers: {
        Accept: 'application/json',
        Authorization: `token ${token}`,
      },
    })
      .then(response => response.json())
      .then(json => dispatch(receiveSubject(json)));
  };
}

export function addSubjectRequest() {
  return {
    type: ADD_SUBJECT_REQUEST,
  };
}

export function addSubjectSuccess(subject) {
  return dispatch => {
    dispatch(NotificationActions.addNotification(
      {
        message: 'Subject Added',
        level: 'success',
        autoDismiss: 2,
      }
    ));
    dispatch(setAddSubjectMode());
    dispatch({
      type: ADD_SUBJECT_SUCCESS,
      isSaving: false,
      subject,
    });
  };
}

export function addSubjectFailure(error) {
  const errors = error.errors;
  return {
    type: ADD_SUBJECT_FAILURE,
    errors,
  };
}

export function addSubject(protocolId, subject) {
  return dispatch => {
    dispatch(addSubjectRequest());
    const url = `api/protocols/${protocolId}/subjects/create`;
    return fetch(url, {
      method: 'POST',
      headers: {
        Accept: 'application/json',
        Authorization: `token ${token}`,
        'X-CSRFToken': csrf_token,
      },
      body: JSON.stringify(subject),
    })
      .then(response => response.json())
      .then(checkAddSubject)
      .then(sub => dispatch(addSubjectSuccess(sub)))
      .catch(errors => dispatch(addSubjectFailure(errors)));
  };
}

export function updateSubjectRequest() {
  return {
    type: UPDATE_SUBJECT_REQUEST,
    isSaving: true,
  };
}

export function updateSubjectFailure(errors) {
  return {
    type: UPDATE_SUBJECT_FAILURE,
    isSaving: false,
    errors,
  };
}

export function updateSubjectSuccess(subject) {
  return dispatch => {
    dispatch({
      type: UPDATE_SUBJECT_SUCCESS,
      isFetching: false,
      subject,
    });
    dispatch(NotificationActions.addNotification(
      {
        message: 'Subject Updated',
        level: 'success',
        autoDismiss: 2,
      }
    ));
    dispatch(NotificationActions.renderNotification());
  };
}

export function updateSubject(protocolId, subject) {
  return dispatch => {
    dispatch(updateSubjectRequest());
    const url = `api/protocols/${protocolId}/subjects/${subject.id}`;
    return fetch(url, {
      method: 'PUT',
      headers: {
        Accept: 'application/json',
        Authorization: `token ${token}`,
        'X-CSRFToken': csrf_token,
      },
      body: JSON.stringify(subject),
    })
      .then(checkStatus)
      .then(response => response.json())
      .then(json => dispatch(updateSubjectSuccess(json)))
      .catch(errors => dispatch(updateSubjectFailure(errors)));
  };
}

export function setLinkMode(mode = null) {
  return {
    type: SET_LINK_MODE,
    mode,
  };
}

export function requestSubjectRecords() {
  return {
    type: REQUEST_SUBJECT_RECORDS,
  };
}

export function receiveSubjectRecords(pds, json) {
  return {
    type: RECEIVE_SUBJECT_RECORDS,
    pds,
    items: json,
  };
}

export function setNewSubjectFormErrors(errors) {
  return {
    type: SET_NEW_SUBJECT_FORM_ERRORS,
    errors,
  };
}

export function fetchSubjectRecords(pds, subject) {
  return dispatch => {
    dispatch(requestSubjectRecords());
    const url = `api/protocoldatasources/${pds.id}/subjects/${subject.id}/records/`;
    return fetch(url, {
      method: 'GET',
      headers: {
        Accept: 'application/json',
        Authorization: `token ${token}`,
      },
    })
      .then(response => response.json())
      .then(json => dispatch(receiveSubjectRecords(pds, json)));
  };
}

export function setUpdateFormErrors(errors) {
  return {
    type: SET_UPDATE_FORM_ERRORS,
    errors,
  };
}
