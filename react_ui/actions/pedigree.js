export const REQUEST_PEDIGREE = 'REQUEST_PEDIGREE';
export const RECEIVE_PEDIGREE = 'RECEIVE_PEDIGREE';
export const SET_ACTIVE_PEDIGREE = 'SET_ACTIVE_PEDIGREE'

export function requestPedigree() {
  return {
    type: REQUEST_PEDIGREE,
  };
}

export function receivePedigree(json) {
  return {
    type: REQUEST_PEDIGREE_SUCCESS,
    pedigree: json,
  };
}

export function fetchPedigree(protocolID, subjectId) {
  const url = `protocols/${protocolID}/pedigree/subject/${subjectID}/`;
  return dispatch => {
    dispatch(requestPedigree());
    return fetch(url, {
      method: 'GET',
      headers: {
        Accept: 'application/json',
        Authorization: `token ${token}`,
      },
    })
      .then(response => response.json())
      .then(json => dispatch(receivePedigree(json)));
  };
}

export function setActivePedigree(pedigree) {
  return {
    type: SET_ACTIVE_PEDIGREE,
    activePedigree: pedigree,
  };
}
