import {
  ADD_MANUSCRIPT_ALTERNATIVE,
  ADD_MANUSCRIPT_ITEM, ADD_PROMISE_TO_ALTERNATIVE, CHANGE_MANUSCRIPT_ALTERNATIVE_PROPERTY,
  CHANGE_MANUSCRIPT_ITEM_PROPERTY, CHANGE_MANUSCRIPT_PROPERTY, CREATE_MANUSCRIPT, DELETE_MANUSCRIPT_ITEM,
  EDIT_MANUSCRIPT,
  LOAD_MANUSCRIPT, MOVE_MANUSCRIPT_ITEM, POST_MANUSCRIPT, REMOVE_PROMISE_FROM_ALTERNATIVE
} from "../reducers/current_manuscript";

export const addManuscriptAlternative = () => {
  return {
    type: ADD_MANUSCRIPT_ALTERNATIVE
  };
};

export const addManuscriptItem = (itemText = 'Ny tekst', itemType = 'text') => {
  return {
    type: ADD_MANUSCRIPT_ITEM,
    itemText,
    itemType
  };
};

export const addPromiseToAlternative = (alternativeIndex, promise, promiseId) => {
  return {
    type: ADD_PROMISE_TO_ALTERNATIVE,
    alternativeIndex,
    promise,
    promiseId
  };
};

export const changeManuscriptAlternativeProperty = (index, propertyName, value) => {
  return {
    type: CHANGE_MANUSCRIPT_ALTERNATIVE_PROPERTY,
    index,
    propertyName,
    value
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
  };
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
  };
};

export const editManuscript = (manuscript, json) => {
  return {
    type: EDIT_MANUSCRIPT,
    manuscript,
    json
  };
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
  };
};

export const postManuscript = (manuscript, json) => {
  return {
    type: POST_MANUSCRIPT,
    manuscript,
    json
  };
};

export const removePromiseFromAlternative = (alternativeIndex, promise) => {
  return {
    type: REMOVE_PROMISE_FROM_ALTERNATIVE,
    alternativeIndex,
    promise
  };
};
