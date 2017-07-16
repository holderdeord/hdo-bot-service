import {
  ADD_MANUSCRIPT,
  ADD_MANUSCRIPT_ITEM,
  CHANGE_MANUSCRIPT_ITEM_PROPERTY,
  CHANGE_MANUSCRIPT_PROPERTY, DELETE_MANUSCRIPT,
  DELETE_MANUSCRIPT_ITEM, EDIT_MANUSCRIPT, LOAD_MANUSCRIPTS, MOVE_MANUSCRIPT_ITEM, POST_MANUSCRIPT
} from "../reducers/manuscripts";
import { ManuscriptTypeEnum } from "../utils/enums";

export const addManuscript = (name = 'Nytt manuskript', manuscriptType = ManuscriptTypeEnum.Info.key, items = []) => {
  return {
    type: ADD_MANUSCRIPT,
    pk: -1,
    name,
    manuscriptType,
    items
  };
};

export const addManuscriptItem = (manuscriptId, itemText = 'Ny tekst', itemType = 'text') => {
  return {
    type: ADD_MANUSCRIPT_ITEM,
    manuscriptId,
    itemText,
    itemType
  };
};

export const changeManuscriptItemProperty = (manuscriptId, order, propertyName, value) => {
  return {
    type: CHANGE_MANUSCRIPT_ITEM_PROPERTY,
    manuscriptId,
    order,
    propertyName,
    value
  }
};

export const changeManuscriptProperty = (manuscriptId, propertyName, value) => {
  return {
    type: CHANGE_MANUSCRIPT_PROPERTY,
    manuscriptId,
    propertyName,
    value
  }
};

export const deleteManuscript = (manuscriptId, json) => {
  return {
    type: DELETE_MANUSCRIPT,
    manuscriptId,
    json
  }
};

export const deleteManuscriptItem = (manuscriptId, order) => {
  return {
    type: DELETE_MANUSCRIPT_ITEM,
    manuscriptId,
    order
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

export const moveManuscriptItem = (manuscriptId, order, move) => {
  return {
    type: MOVE_MANUSCRIPT_ITEM,
    manuscriptId,
    order,
    move
  }
};

export const postManuscript = (manuscript, json) => {
  return {
    type: POST_MANUSCRIPT,
    manuscript,
    json
  }
};