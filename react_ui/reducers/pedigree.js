import { REQUEST_PEDIGREE, RECEIVE_PEDIGREE, SET_ACTIVE_PEDIGREE,
         CLEAR_PEDIGREE_STATE, SET_ADD_PEDIGREE_REL, SET_ADD_PEDIGREE_REL_MODE,
         ADD_PEDIGREE_REL_SUCCESS, ADD_PEDIGREE_REL_REQUEST,
         ADD_PEDIGREE_REL_FAILURE, SET_UPDATE_FORM_ERRORS} from '../actions/pedigree';

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
        activePedigreeId: parseInt(action.pedigreeId, 10),
      });
    case CLEAR_PEDIGREE_STATE:
      return initialState;
    case SET_ADD_PEDIGREE_REL:
      return Object.assign({}, state, {
        newPedigreeRel: action.pedigreeRel,
      });
    case SET_ADD_PEDIGREE_REL_MODE:
      if (action.mode != null) {
        return Object.assign({}, state, {
          addPedigreeRelMode: action.mode,
        });
      }
      return Object.assign({}, state, {
        addPedigreeRelMode: !action.mode,
      });
    case ADD_PEDIGREE_REL_REQUEST:
      return Object.assign({}, state, {
        isSaving: true,
      });
    case ADD_PEDIGREE_REL_SUCCESS:
      return Object.assign({}, state, {
        newFormErrors: {
          server: [],
          form: [],
        },
        isSaving: false,
      });
    case ADD_PEDIGREE_REL_FAILURE:
      return Object.assign({}, state, {
        newFormErrors: {
          server: action.errors,
          form: [],
        },
        isSaving: false,
      });
    case SET_UPDATE_FORM_ERRORS:
      return Object.assign({}, state, {
        updateFormErrors: {
          server: [],
          form: action.errors,
        },
      });
  default:
    return state;
  }
}

export default pedigree;
