import {
  ADD_MANUSCRIPT,
  ADD_MANUSCRIPT_ITEM,
  CHANGE_MANUSCRIPT_ITEM_PROPERTY,
  CHANGE_MANUSCRIPT_PROPERTY,
  DELETE_MANUSCRIPT_ITEM, EDIT_MANUSCRIPT, LOAD_MANUSCRIPT, POST_MANUSCRIPT
} from "../reducers/manuscripts";
import { ManuscriptTypeEnum } from "../utils/enums";

export const addManuscript = (name = 'Nytt manuskript', manuscriptType = ManuscriptTypeEnum.Info.key, items = []) => {
  return {
    type: ADD_MANUSCRIPT,
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

export const loadManuscript = (manuscriptId, manuscript) => {
  return {
    type: LOAD_MANUSCRIPT,
    manuscriptId,
    manuscript
  }
};

export const postManuscript = (manuscript, json) => {
  return {
    type: POST_MANUSCRIPT,
    manuscript,
    json
  }
};