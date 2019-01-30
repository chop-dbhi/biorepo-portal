import { REQUEST_PEDIGREE, RECEIVE_PEDIGREE, SET_ACTIVE_PEDIGREE, CLEAR_PEDIGREE_STATE } from '../actions/pedigree';

const initialState = {
  isFetching: false,
  items: [],
};

function pedigree(state = initialState, action){
  switch (action.type) {
    case REQUEST_PEDIGREE:
      return Object.assign({}, state, {
        items: [],
        isFetching: true,
      });
    case RECEIVE_PEDIGREE:
      return Object.assign({}, state, {
        isFetching: false,
        items: action.pedigree,
      });
    case SET_ACTIVE_PEDIGREE:
      return Object.assign({}, state, {
        activeProtocolId: parseInt(action.pedigreeId, 10),
      });
    case CLEAR_PEDIGREE_STATE:
      return initialState;
  default:
    return state;
  }
}

export default pedigree;
