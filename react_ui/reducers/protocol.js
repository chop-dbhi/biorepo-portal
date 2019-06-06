import { REQUEST_PROTOCOLS, RECEIVE_PROTOCOLS, SET_ACTIVE_PROTOCOL, REQUEST_PROTOCOL_ORGS,
         RECEIVE_PROTOCOL_ORGS, RECEIVE_PROTOCOL } from '../actions/protocol';

const initialState = [{
  isFetching: false,
  items: [],
  activeProtocolId: null,
  orgs: [],
}];

function protocol(state=initialState, action) {
  switch (action.type) {
    case REQUEST_PROTOCOLS:
      return Object.assign({}, state, {
        items: [],
        isFetching: true,
      });
    case RECEIVE_PROTOCOLS:
      return Object.assign({}, state, {
        isFetching: false,
        items: action.protocols,
      });
    case SET_ACTIVE_PROTOCOL:
      return Object.assign({}, state, {
        activeProtocolId: parseInt(action.protocolId, 10),
      });
    case REQUEST_PROTOCOL_ORGS:
      return Object.assign({}, state, {
        isFetching: true,
      });
    case RECEIVE_PROTOCOL_ORGS:
      return Object.assign({}, state, {
        orgs: action.organizations,
        isFetching: false,
      });
    case RECEIVE_PROTOCOL:
      return Object.assign({}, state, {
        items: action.items,
      });

    default:
      return state;
  }
}

export default protocol;
