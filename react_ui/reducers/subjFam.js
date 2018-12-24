import { REQUEST_SUBJ_FAM, RECEIVE_SUBJ_FAM, SET_ACTIVE_SUBJ_FAM,
         CLEAR_SUBJ_FAM_STATE, SET_ADD_SUBJ_FAM_REL, SET_ADD_SUBJ_FAM_REL_MODE,
         ADD_SUBJ_FAM_REL_SUCCESS, ADD_SUBJ_FAM_REL_REQUEST,
         ADD_SUBJ_FAM_REL_FAILURE, SET_UPDATE_FORM_ERRORS, RECEIVE_RELATIONSHIP_TYPES,
         REQUEST_RELATIONSHIP_TYPES} from '../actions/subjFam';

const initialState = {
  isFetching: false,
  items: [],
};

function subjFam(state = initialState, action){
  switch (action.type) {
    case REQUEST_SUBJ_FAM:
      return Object.assign({}, state, {
        items: [],
        isFetching: true,
      });
    case RECEIVE_SUBJ_FAM:
      return Object.assign({}, state, {
        isFetching: false,
        items: action.subjFam,
      });
    case REQUEST_RELATIONSHIP_TYPES:
      return Object.assign({}, state, {
        relTypes: [],
        isFetching: true,
      });
    case RECEIVE_RELATIONSHIP_TYPES:
      return Object.assign({}, state, {
        isFetching: false,
        relTypes: action.relTypes
      })
    case SET_ACTIVE_SUBJ_FAM:
      return Object.assign({}, state, {
        activeSubjFamId: parseInt(action.subjFamId, 10),
      });
    case CLEAR_SUBJ_FAM_STATE:
      return initialState;
    case SET_ADD_SUBJ_FAM_REL:
      return Object.assign({}, state, {
        newSubjFamRel: action.subjFamRel,
      });
    case SET_ADD_SUBJ_FAM_REL_MODE:
      if (action.mode != null) {
        return Object.assign({}, state, {
          addSubjFamRelMode: action.mode,
        });
      }
      return Object.assign({}, state, {
        addSubjFamRelMode: !action.mode,
      });
    case ADD_SUBJ_FAM_REL_REQUEST:
      return Object.assign({}, state, {
        isSaving: true,
      });
    case ADD_SUBJ_FAM_REL_SUCCESS:
      return Object.assign({}, state, {
        newFormErrors: {
          server: [],
          form: [],
        },
        isSaving: false,
        addSubjFamRelMode: false,
      });
    case ADD_SUBJ_FAM_REL_FAILURE:
      return Object.assign({}, state, {
        newFormErrors: {
          server: action.errors,
          form: [],
        },
        isSaving: false,
      });
    case SET_UPDATE_FORM_ERRORS:
      return Object.assign({}, state, {
        updateFormErrors: action.error,
      });
  default:
    return state;
  }
}

export default subjFam;
