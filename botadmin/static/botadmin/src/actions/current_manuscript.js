import {
  ADD_MANUSCRIPT_ITEM,
  CHANGE_MANUSCRIPT_ITEM_PROPERTY, CHANGE_MANUSCRIPT_PROPERTY, CREATE_MANUSCRIPT, DELETE_MANUSCRIPT_ITEM,
  LOAD_MANUSCRIPT, MOVE_MANUSCRIPT_ITEM
} from "../reducers/current_manuscript";

export const addManuscriptItem = (itemText = 'Ny tekst', itemType = 'text') => {
  return {
    type: ADD_MANUSCRIPT_ITEM,
    itemText,
    itemType
  };
};

export const changeManuscriptItemProperty = (order, propertyName, value) => {
  return {
    type: CHANGE_MANUSCRIPT_ITEM_PROPERTY,
    order,
    propertyName,
    value
  }
};

export const changeManuscriptProperty = (propertyName, value) => {
  return {
    type: CHANGE_MANUSCRIPT_PROPERTY,
    propertyName,
    value
  }
};

export const createManuscript = () => {
  return {
    type: CREATE_MANUSCRIPT
  };
};

export const deleteManuscriptItem = (order) => {
  return {
    type: DELETE_MANUSCRIPT_ITEM,
    order
  }
};

export const loadManuscript = (json) => {
  return {
    type: LOAD_MANUSCRIPT,
    json
  };
};

export const moveManuscriptItem = (order, move) => {
  return {
    type: MOVE_MANUSCRIPT_ITEM,
    order,
    move
  }
};
