import { REQUEST_SUBJ_FAM, RECEIVE_SUBJ_FAM, SET_ACTIVE_SUBJ_FAM_REL,
         CLEAR_SUBJ_FAM_STATE, SET_ADD_SUBJ_FAM_REL, SET_ADD_SUBJ_FAM_REL_MODE,
         ADD_SUBJ_FAM_REL_SUCCESS, ADD_SUBJ_FAM_REL_REQUEST,
         ADD_SUBJ_FAM_REL_FAILURE, SET_UPDATE_FORM_ERRORS, RECEIVE_RELATIONSHIP_TYPES,
         REQUEST_RELATIONSHIP_TYPES, SET_EDIT_SUBJ_FAM_REL_MODE,
         EDIT_SUBJ_FAM_REL_REQUEST, EDIT_SUBJ_FAM_REL_FAILURE,
         EDIT_SUBJ_FAM_REL_SUCCESS, SET_DELETE_SUBJ_FAM_REL_MODE} from '../actions/subjFam';

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
    case SET_ACTIVE_SUBJ_FAM_REL:
      return Object.assign({}, state, {
        activeSubjFam: action.activeSubjFam,
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
    case SET_EDIT_SUBJ_FAM_REL_MODE:
      if (action.mode != null) {
        return Object.assign({}, state, {
          editSubjFamRelMode: action.mode,
        });
      }
      return Object.assign({}, state, {
        editSubjFamRelMode: !action.mode,
      });
    case EDIT_SUBJ_FAM_REL_REQUEST:
      return Object.assign({}, state, {
        isSaving: true,
      });
    case EDIT_SUBJ_FAM_REL_SUCCESS:
      return Object.assign({}, state, {
        newFormErrors: {
          server: [],
          form: [],
        },
        isSaving: false,
        editSubjFamRelMode: false,
      });
    case EDIT_SUBJ_FAM_REL_FAILURE:
      return Object.assign({}, state, {
        newFormErrors: {
          server: action.errors,
          form: [],
        },
        isSaving: false,
      });
    case SET_DELETE_SUBJ_FAM_REL_MODE:
      if (action.mode != null) {
        return Object.assign({}, state, {
          deleteSubjFamRelMode: action.mode,
        });
      }
      return Object.assign({}, state, {
        deleteSubjFamRelMode: !action.mode,
      });
  default:
    return state;
  }
}

export default subjFam;
