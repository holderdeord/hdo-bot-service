import {
  DELETE_MANUSCRIPT,
  LOAD_MANUSCRIPTS,
  SORT_MANUSCRIPTS
} from "../reducers/manuscripts";

export const deleteManuscript = (manuscriptId, json) => {
  return {
    type: DELETE_MANUSCRIPT,
    manuscriptId,
    json
  }
};

export const loadManuscripts = (manuscripts) => {
  return {
    type: LOAD_MANUSCRIPTS,
    manuscripts
  }
};

export const sortManuscripts = (fieldName) => {
  return {
    type: SORT_MANUSCRIPTS,
    fieldName
  }
};