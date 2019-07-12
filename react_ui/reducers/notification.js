import { ADD_NOTIFICATION, REMOVE_NOTIFICATION,
         RENDER_NOTIFICATION } from '../actions/notification';

const initialState = [
  { items: [] }];

let notifications = [];

function notification(state = initialState, action) {
  switch (action.type) {
    case RENDER_NOTIFICATION:
      return Object.assign({}, state, {
        items: [],
      });
    case ADD_NOTIFICATION:
      return Object.assign({}, state, {
        items: state.items.concat(action.notification),
      });
    case REMOVE_NOTIFICATION:
      notifications = state.items.filter((note) => {
        if (note.message !== action.notification.message) {
          return notification;
        }
        return null;
      });

      return Object.assign({}, state, {
        items: notifications,
      });
    default:
      return state;
  }
}

export default notification;
