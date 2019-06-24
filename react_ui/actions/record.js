/* global token csrf_token*/
/* eslint no-param-reassign: ["error", { "props": false }]*/
export const SET_ACTIVE_RECORD = 'SET_ACTIVE_RECORD';
export const REQUEST_LABELS = 'REQUEST_LABELS';
export const RECEIVE_LABELS = 'RECEIVE_LABELS';
export const REQUEST_RECORD_LINKS = 'REQUEST_RECORD_LINKS';
export const RECEIVE_RECORD_LINKS = 'RECEIVE_RECORD_LINKS';
export const RECEIVE_RECORDS = 'RECEIVE_RECORDS';
export const REQUEST_RECORDS = 'REQUEST_RECORDS';
export const SET_EDIT_LABEL_MODE = 'SET_EDIT_LABEL_MODE';
export const SET_SELECTED_LABEL = 'SET_SELECTED_LABEL';
export const CLEAR_RECORD_STATE = 'CLEAR_RECORD_STATE';
export const SET_PENDING_LINKED_RECORD = 'SET_PENDING_LINKED_RECORD';
export const SET_SELECTED_LINK_TYPE = 'SET_SELECTED_LINK_TYPE';
export const UPDATE_RECORD_REQUEST = 'UPDATE_RECORD_REQUEST';
export const UPDATE_RECORD_FAILURE = 'UPDATE_RECORD_FAILURE';
export const UPDATE_RECORD_SUCCESS = 'UPDATE_RECORD_SUCCESS';
export const DISMISS_LINK_TYPE_MODAL = 'DISMISS_LINK_TYPE_MODAL';
export const CREATE_RECORD_REQUEST = 'CREATE_RECORD_REQUEST';
export const SET_RECORD_ERROR = 'SET_RECORD_ERROR';
export const SET_ADD_RECORD_MODE = 'SET_ADD_RECORD_MODE';
export const CREATE_RECORD_LINK_REQUEST = 'CREATE_RECORD_LINK_REQUEST';
export const CREATE_RECORD_LINK_SUCCESS = 'CREATE_RECORD_LINK_SUCCESS';
export const CREATE_RECORD_LINK_FAILURE = 'CREATE_RECORD_LINK_FAILURE';
export const DELETE_RECORD_LINK_REQUEST = 'DELETE_RECORD_LINK_REQUEST';
export const DELETE_RECORD_LINK_SUCCESS = 'DELETE_RECORD_LINK_SUCCESS';
export const DELETE_RECORD_LINK_FAILURE = 'DELETE_RECORD_LINK_FAILURE';
import * as NotificationActions from './notification';
import * as SubjectActions from './subject';

function checkStatus(response) {
  if (response.status >= 200 && response.status < 300) {
    return response;
  }
  const error = new Error(response.statusText);
  error.response = response;
  return error;
}

function checkLinkAction(json) {
  if (json.success) {
    return json;
  }
  const error = new Error(json.error);
  throw error;
}

export function setAddRecordMode(mode = null) {
  return {
    type: SET_ADD_RECORD_MODE,
    mode,
  };
}

export function clearRecordState() {
  return {
    type: CLEAR_RECORD_STATE,
  };
}

export function createRecordRequest() {
  return {
    type: CREATE_RECORD_REQUEST,
    isCreating: true,
  };
}

export function setRecordError(error) {
  return {
    type: SET_RECORD_ERROR,
    error,
  };
}

export function setActiveRecord(record) {
  return {
    type: SET_ACTIVE_RECORD,
    activeRecord: record,
  };
}

export function setPendingLinkedRecord(record) {
  return {
    type: SET_PENDING_LINKED_RECORD,
    record,
  };
}

export function setSelectedLinkType(linkId) {
  return {
    type: SET_SELECTED_LINK_TYPE,
    linkId,
  };
}

export function setSelectedLabel(labelId) {
  return {
    type: SET_SELECTED_LABEL,
    selectedLabel: labelId,
  };
}

export function requestLabels() {
  return {
    type: REQUEST_LABELS,
    labels: [],
    isFetching: true,
  };
}

export function receiveLabels(json) {
  return {
    type: RECEIVE_LABELS,
    labels: json,
    isFetching: false,
    receivedAt: Date.now(),
  };
}

export function requestRecords() {
  return {
    type: REQUEST_RECORDS,
  };
}

export function receiveRecords(pds, json) {
  const records = json.map(record => {
    record.pds = pds.id;
    // Map record label descriptions
    pds.driver_configuration.labels.forEach(label => {
      if (label[0] === record.label) {
        record.label_desc = label[1];
      }
    });
    return record;
  });
  return {
    type: RECEIVE_RECORDS,
    items: records,
    pds,
  };
}

export function updateRecordRequest() {
  return {
    type: UPDATE_RECORD_REQUEST,
  };
}

export function updateRecordSuccess(record) {
  return dispatch => {
    dispatch({
      type: UPDATE_RECORD_SUCCESS,
      isFetching: false,
      record,
    });
    // dispatch(NotificationActions.addNotification(
    //   {
    //     message: 'Record Updated',
    //     level: 'success',
    //     autoDismiss: 2,
    //   }
    // ));
    // dispatch(NotificationActions.renderNotification());
  };
}

export function updateRecord(pdsId, subjectId, record) {
  const url = `api/protocoldatasources/${pdsId}/subjects/${subjectId}/record/${record.id}/`;
  return dispatch => {
    dispatch(updateRecordRequest());
    fetch(url, {
      method: 'PUT',
      headers: {
        Accept: 'application/json',
        Authorization: `token ${token}`,
        'X-CSRFToken': csrf_token,
      },
      body: JSON.stringify(record),
    })
      .then(checkStatus)
      .then(response => response.json())
      .then(json => dispatch(updateRecordSuccess(json)));
  };
}

export function fetchRecords(pds, subjectId) {
  const url = `api/protocoldatasources/${pds.id}/subjects/${subjectId}/records/`;
  return dispatch => {
    // If not authorized don't bother requesting records
    if (!pds.authorized) {
      return dispatch(receiveRecords(pds, []));
    }
    dispatch(requestRecords());
    return fetch(url, {
      method: 'GET',
      headers: {
        Accept: 'application/json',
        Authorization: `token ${token}`,
      },
    })
      .then(response => response.json())
      .then(json => dispatch(receiveRecords(pds, json)));
  };
}

export function setEditLabelMode(mode = null) {
  return {
    type: SET_EDIT_LABEL_MODE,
    mode,
  };
}

export function requestRecordLinks() {
  return {
    type: REQUEST_RECORD_LINKS,
  };
}

export function receiveRecordLinks(json) {
  return {
    type: RECEIVE_RECORD_LINKS,
    links: json,
  };
}

export function dismissLinkModal() {
  return {
    type: DISMISS_LINK_TYPE_MODAL,
  };
}

export function fetchRecordLinks(pdsId, subjectId, recordId) {
  const url = `api/protocoldatasources/${pdsId}/subjects/${subjectId}/record/${recordId}/links/`;
  return dispatch => {
    dispatch(requestRecordLinks());
    return fetch(url, {
      method: 'GET',
      headers: {
        Accept: 'application/json',
        Authorization: `token ${token}`,
      },
    })
      .then(response => response.json())
      .then(json => dispatch(receiveRecordLinks(json)));
  };
}

export function createRecordLinkRequest() {
  return {
    type: CREATE_RECORD_LINK_REQUEST,
  };
}

export function createRecordLinkSuccess(json, pds, subjectId, recordId) {
  return dispatch => {
    dispatch(fetchRecordLinks(pds, subjectId, recordId));
    dispatch(dismissLinkModal());
    dispatch(SubjectActions.setLinkMode(false));
    dispatch({
      type: CREATE_RECORD_LINK_SUCCESS,
    });
  };
}

export function createRecordLinkFailure(error) {
  return {
    type: CREATE_RECORD_LINK_FAILURE,
    error,
  };
}

export function createRecordLink(primaryRecord, secondaryRecord) {
  return (dispatch, getState) => {
    const state = getState();
    const url = `api/protocoldatasources/${primaryRecord.pds}/subjects/` +
    `${state.subject.activeSubject.id}/record/${primaryRecord.id}/links/`;
    dispatch(createRecordLinkRequest());
    const data = {
      primaryRecord,
      secondaryRecord,
      linkType: state.record.selectedLinkType,
    };
    fetch(url, {
      method: 'POST',
      headers: {
        Accept: 'application/json',
        Authorization: `token ${token}`,
        'Content-Type': 'application/json',
        'X-CSRFToken': csrf_token,
      },
      body: JSON.stringify(data),
    })
      .then(response => response.json())
      .then(checkLinkAction)
      .then(json => dispatch(
        createRecordLinkSuccess(
          json, primaryRecord.pds, state.subject.activeSubject.id, primaryRecord.id)))
      .catch(error => dispatch(createRecordLinkFailure(error)));
  };
}

export function deleteRecordLinkRequest() {
  return {
    type: DELETE_RECORD_LINK_REQUEST,
  };
}

export function deleteRecordLinkSuccess(json, linkId) {
  return {
    type: DELETE_RECORD_LINK_SUCCESS,
    linkId,
  };
}

export function deleteRecordLinkFailure(error) {
  return {
    type: DELETE_RECORD_LINK_FAILURE,
    error,
  };
}

export function deleteRecordLink(primaryRecord, linkId) {
  return (dispatch, getState) => {
    const state = getState();
    dispatch(deleteRecordLinkRequest());
    const url = `api/protocoldatasources/${primaryRecord.pds}/subjects/` +
    `${state.subject.activeSubject.id}/record/${primaryRecord.id}/links/`;
    const data = {
      primaryRecord,
      linkId,
    };
    fetch(url, {
      method: 'DELETE',
      headers: {
        Accept: 'application/json',
        Authorization: `token ${token}`,
        'X-CSRFToken': csrf_token,
      },
      body: JSON.stringify(data),
    })
      .then(response => response.json())
      .then(checkLinkAction)
      .then(json => dispatch(deleteRecordLinkSuccess(json, linkId)))
      .catch(error => dispatch(deleteRecordLinkFailure(error)));
  };
}
