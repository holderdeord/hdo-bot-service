import { combineReducers } from 'redux';
import manuscripts from "./manuscripts";
import manuscriptItems from "./manuscriptItems";

export const adminApp = combineReducers({
  manuscripts,
  manuscriptItems
});
