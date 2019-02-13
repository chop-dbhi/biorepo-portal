/* global token*/
import fetch from 'isomorphic-fetch';
import * as PDSActions from './pds';

export const SET_ACTIVE_PROTOCOL = 'SET_ACTIVE_PROTOCOL';
export const REQUEST_PROTOCOLS = 'REQUEST_PROTOCOLS';
export const RECEIVE_PROTOCOLS = 'RECEIVE_PROTOCOLS';
export const REQUEST_PROTOCOL = 'REQUEST_PROTOCOL';
export const RECEIVE_PROTOCOL = 'RECEIVE_PROTOCOL';
export const REQUEST_PROTOCOL_ORGS = 'REQUEST_PROTOCOL_ORGS';
export const RECEIVE_PROTOCOL_ORGS = 'RECEIVE_PROTOCOL_ORGS';


export function requestProtocols() {
  return {
    type: REQUEST_PROTOCOLS,
  };
}

export function receiveProtocols(json) {
  return {
    type: RECEIVE_PROTOCOLS,
    protocols: json,
    receivedAt: Date.now(),
  };
}

export function requestOrganizations() {
  return {
    type: REQUEST_PROTOCOL_ORGS,
  };
}

export function receiveOrganizations(json) {
  return {
    type: RECEIVE_PROTOCOL_ORGS,
    organizations: json,
  };
}

export function fetchOrganizations(protocolId) {
  const url = `api/protocols/${protocolId}/organizations/`;
  return dispatch => {
    dispatch(requestOrganizations());
    return fetch(url, {
      method: 'GET',
      headers: {
        Accept: 'application/json',
        Authorization: `token ${token}`,
      },
    })
      .then(response => response.json())
      .then(json => dispatch(receiveOrganizations(json)));
  };
}

export function setActiveProtocol(protocolId) {
  return dispatch => {
    // If there is an active protocol fetch its organizations and PDS
    if (protocolId != null) {
      dispatch(fetchOrganizations(protocolId));
      // Refresh PDS for the select Protocol
      dispatch(PDSActions.fetchPDS(protocolId));
      // get protocol details
      dispatch(fetchProtocol(protocolId));
    }
    // Update our state with the Protocol given
    dispatch({
      type: SET_ACTIVE_PROTOCOL,
      protocolId,
    });
  };
}

export function requestProtocol() {
  return {
    type: REQUEST_PROTOCOL,
  };
}

export function receiveProtocol(json) {
  return dispatch => {
    dispatch({
      type: RECEIVE_PROTOCOL,
      items: json,
    });
  };
}

export function fetchProtocols() {
  // Fetch protocols authorized for authorized user.
  return dispatch => {
    dispatch(requestProtocols());
    return fetch('api/protocols/', {
      method: 'GET',
      headers: {
        Accept: 'application/json',
        Authorization: `token ${token}`,
      },
    })
      .then(response => response.json())
      .then(json => dispatch(receiveProtocols(json)));
  };
}

export function fetchProtocol(protocolId) {
  // Fetch protocols authorized for authorized user.
  return dispatch => {
    dispatch(requestProtocol());
    const url = `api/protocols/${protocolId}/`;
    return fetch(url, {
      method: 'GET',
      headers: {
        Accept: 'application/json',
        Authorization: `token ${token}`,
      },
    })
      .then(response => response.json())
      .then(json => dispatch(receiveProtocol(json)));
  };
}
