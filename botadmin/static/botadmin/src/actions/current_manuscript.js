import { CREATE_MANUSCRIPT, LOAD_MANUSCRIPT } from "../reducers/current_manuscript";

export const createManuscript = () => {
  return {
    type: CREATE_MANUSCRIPT
  };
};

export const loadManuscript = (manuscriptId, json) => {
  return {
    type: LOAD_MANUSCRIPT,
    manuscriptId,
    json
  };
};