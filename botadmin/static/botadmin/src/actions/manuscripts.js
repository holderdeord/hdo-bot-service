import {
  DELETE_MANUSCRIPT,
  EDIT_MANUSCRIPT,
  LOAD_MANUSCRIPTS,
  POST_MANUSCRIPT, SORT_MANUSCRIPTS
} from "../reducers/manuscripts";

export const deleteManuscript = (manuscriptId, json) => {
  return {
    type: DELETE_MANUSCRIPT,
    manuscriptId,
    json
  }
};

export const editManuscript = (manuscript, json) => {
  return {
    type: EDIT_MANUSCRIPT,
    manuscript,
    json
  }
};

export const loadManuscripts = (manuscripts) => {
  return {
    type: LOAD_MANUSCRIPTS,
    manuscripts
  }
};

export const postManuscript = (manuscript, json) => {
  return {
    type: POST_MANUSCRIPT,
    manuscript,
    json
  }
};

export const sortManuscripts = (fieldName) => {
  return {
    type: SORT_MANUSCRIPTS,
    fieldName
  }
};