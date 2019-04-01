import { combineReducers } from 'redux';
import protocol from './protocol';
import subject from './subject';
import pds from './pds';
import record from './record';
import notification from './notification';
import subjFam from './subjFam';

const rootReducer = combineReducers({
  protocol,
  subject,
  pds,
  record,
  notification,
  subjFam,
});

export default rootReducer;
