import { combineReducers } from 'redux';
import manuscripts from "./manuscripts";
import current_manuscript from "./current_manuscript";

export const adminApp = combineReducers({
  current_manuscript,
  manuscripts
});
