import { closePromisesModal, openPromisesModal } from "../actions/promises_modal";
export const handleAndDispatchPromisesModal = (dispatch, match) => {
  if (match.params.alternativeIndex) {
    const alternativeIndex = parseInt(match.params.alternativeIndex, 10);
    dispatch(openPromisesModal(alternativeIndex));
  } else {
    dispatch(closePromisesModal());
  }
};