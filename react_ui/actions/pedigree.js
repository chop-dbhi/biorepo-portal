
import fetch from 'isomorphic-fetch';

export const REQUEST_PEDIGREE = 'REQUEST_PEDIGREE';
export const RECEIVE_PEDIGREE = 'RECEIVE_PEDIGREE';
export const SET_ACTIVE_PEDIGREE = 'SET_ACTIVE_PEDIGREE';

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

export function setActivePedigree(pedigree) {
  return {
    type: SET_ACTIVE_PEDIGREE,
    activePedigree: pedigree,
  };
}
