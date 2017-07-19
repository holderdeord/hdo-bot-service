import { CLOSE_PROMISES_MODAL, OPEN_PROMISES_MODAL } from "../reducers/promises_modal";

export const closePromisesModal = () => {
  return {
    type: CLOSE_PROMISES_MODAL
  };
};

export const openPromisesModal = (alternative_index) => {
  return {
    type: OPEN_PROMISES_MODAL,
    alternative_index
  };
};