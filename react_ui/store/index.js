import { createStore, applyMiddleware, compose } from 'redux';
import thunkMiddleware from 'redux-thunk';
import rootReducer from '../reducers';
import createLogger  from 'redux-logger';

const middlewares = [thunkMiddleware];

if (process.env.NODE_ENV === 'development') {
  const logger = createLogger();
  middlewares.push(logger);
}

const store = compose(applyMiddleware(...middlewares))(createStore)(rootReducer);

// let store = createStore(rootReducer);

export default store;
