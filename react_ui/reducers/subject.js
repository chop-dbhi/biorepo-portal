/* eslint-disable no-param-reassign*/
import { REQUEST_SUBJECTS, RECEIVE_SUBJECTS, SET_ACTIVE_SUBJECT,
         SHOW_INFO_PANEL, HIDE_INFO_PANEL, SHOW_ACTION_PANEL,
         HIDE_ACTION_PANEL, UPDATE_SUBJECT_SUCCESS, UPDATE_SUBJECT_REQUEST,
         SET_LINK_MODE, ADD_SUBJECT_SUCCESS, ADD_SUBJECT_FAILURE,
         SET_ADD_SUBJECT_MODE, SET_NEW_SUBJECT, REQUEST_SUBJECT_SUCCESS,
         SET_NEW_SUBJECT_FORM_ERRORS, SET_UPDATE_FORM_ERRORS,
         UPDATE_SUBJECT_FAILURE, ADD_SUBJECT_REQUEST } from '../actions/subject';

let initialNewSubject = {
  organization: null,
  dob: null,
  first_name: null,
  last_name: null,
  organization_subject_id: null,
  organization_subject_id_validation: null,
  organization_id_label: 'Subject ID',
};

const initialState = {
  isFetching: false,
  items: [],
  activeSubject: null,
  activeSubjectRecords: [],
  newSubject: Object.assign({}, initialNewSubject),
  isSaving: false,
  showInfoPanel: false,
  showActionPanel: false,
  addRecordMode: false,
  linkMode: false,
  newFormErrors: {
    server: [],
    form: [],
  },
  updateFormErrors: {
    server: [],
    form: [],
  },
};

function subject(state = initialState, action) {
  const newSub = Object.assign({}, initialNewSubject);
  switch (action.type) {
    case REQUEST_SUBJECTS:
      return Object.assign({}, state, {
        items: [],
        isFetching: true,
        addSubjectMode: false,
      });
    case RECEIVE_SUBJECTS:

      // Create a validation entry for org subject ID
      action.subjects.forEach((sub) => {
        sub.organization_subject_id_validation = sub.organization_subject_id;
      });
      return Object.assign({}, state, {
        items: action.subjects,
        isFetching: false,
      });
    case REQUEST_SUBJECT_SUCCESS:
      action.subject.organization_subject_id_validation = action.subject.organization_subject_id;
      action.subject.organization = action.subject.organization;
      action.subject.organization_id_label = action.subject.organization_id_label;
      return Object.assign({}, state, {
        items: action.subjects,
        isFetching: false,
        activeSubject: action.subject,
      });
    case SET_ACTIVE_SUBJECT:
      return Object.assign({}, state, {
        activeSubject: action.subject,
      });
    case SET_NEW_SUBJECT:
      return Object.assign({}, state, {
        newSubject: action.subject,
      });
    case SHOW_INFO_PANEL:
      return Object.assign({}, state, {
        showInfoPanel: true,
      });
    case HIDE_INFO_PANEL:
      return Object.assign({}, state, {
        showInfoPanel: false,
      });
    case SHOW_ACTION_PANEL:
      return Object.assign({}, state, {
        showActionPanel: true,
      });
    case HIDE_ACTION_PANEL:
      return Object.assign({}, state, {
        showActionPanel: false,
      });
    case UPDATE_SUBJECT_REQUEST:
      return Object.assign({}, state, {
        isSaving: true,
      });
    case UPDATE_SUBJECT_FAILURE:
      return Object.assign({}, state, {
        isSaving: false,
        updateFormErrors: {
          form: [],
          server: ['Error saving subject. Server error.'],
        },
      });
    case UPDATE_SUBJECT_SUCCESS:
      action.subject.organization_subject_id_validation = action.subject.organization_subject_id;
      action.subject.organization = action.subject.organization;
      action.subject.external_ids = state.activeSubject.external_ids;
      action.subject.external_records = state.activeSubject.external_records;
      return Object.assign({}, state, {
        isSaving: false,
        updateFormErrors: {
          form: [],
          server: [],
        },
        activeSubject: action.subject,
      });
    case SET_LINK_MODE:
      if (action.mode != null) {
        return Object.assign({}, state, {
          linkMode: action.mode,
        });
      }
      return Object.assign({}, state, {
        linkMode: !state.linkMode,
      });
    case SET_ADD_SUBJECT_MODE:
      if (action.mode != null) {
        return Object.assign({}, state, {
          addSubjectMode: action.mode,
          newFormErrors: {
            server: [],
            form: [],
          },
          newSubject: newSub,
        });
      }
      return Object.assign({}, state, {
        addSubjectMode: !state.addSubjectMode,
        newFormErrors: {
          server: [],
          form: [],
        },
        newSubject: newSub,
      });

    case ADD_SUBJECT_REQUEST:
      return Object.assign({}, state, {
        isSaving: true,
      });
    case ADD_SUBJECT_SUCCESS:
      return Object.assign({}, state, {
        newFormErrors: {
          server: [],
          form: [],
        },
        isSaving: false,
      });
    case ADD_SUBJECT_FAILURE:
      return Object.assign({}, state, {
        newFormErrors: {
          server: action.errors,
          form: [],
        },
        isSaving: false,
      });
    case SET_NEW_SUBJECT_FORM_ERRORS:
      return Object.assign({}, state, {
        newFormErrors: {
          server: [],
          form: action.errors,
        },
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

export default subject;
