import { loadHdoCategories } from "../actions/hdo_categories";
import { getHdoCategoriesApiUrl } from "./urls";
export function loadAndDispatchHdoCategories(dispatch) {
  dispatch(loadHdoCategories());
  return fetch(getHdoCategoriesApiUrl())
    .then(response => response.json())
    .then(categories => dispatch(loadHdoCategories(categories)))
    .catch(error => dispatch(loadHdoCategories(error)));
}