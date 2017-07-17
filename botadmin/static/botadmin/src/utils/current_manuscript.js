import { getManuscriptApiUrl } from "./urls";
import { addManuscriptItem, createManuscript, loadManuscript } from "../actions/current_manuscript";

export function createAndDispatchManuscript(dispatch) {
  dispatch(createManuscript());
  dispatch(addManuscriptItem());
}

export function loadAndDispatchManuscript(dispatch, manuscriptId) {
  dispatch(loadManuscript());
  fetch(getManuscriptApiUrl(manuscriptId))
    .then(response => response.json())
    .then(manuscript => dispatch(loadManuscript(manuscript)))
    .catch(error => dispatch(loadManuscript(error)));
}