import { combineReducers } from 'redux';
import manuscripts from "./manuscripts";
import current_manuscript from "./current_manuscript";
import hdo_categories from "./hdo_categories";

export const adminApp = combineReducers({
  current_manuscript,
  hdo_categories,
  manuscripts
});
