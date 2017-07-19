import { combineReducers } from 'redux';
import manuscripts from "./manuscripts";
import current_manuscript from "./current_manuscript";
import hdo_categories from "./hdo_categories";
import promises_modal from "./promises_modal";

export const adminApp = combineReducers({
  current_manuscript,
  hdo_categories,
  manuscripts,
  promises_modal
});
