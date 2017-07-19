export const CLOSE_PROMISES_MODAL = 'CLOSE_PROMISES_MODAL';
export const OPEN_PROMISES_MODAL = 'OPEN_PROMISES_MODAL';

const promises_modal = (state = create_modal(), action) => {
  switch (action.type) {
    case CLOSE_PROMISES_MODAL:
      return create_modal();
    case OPEN_PROMISES_MODAL:
      return {
        ...state,
        alternative_index: action.alternative_index,
        open: true
      };
    default:
      return state;
  }
};

export default promises_modal;

function create_modal() {
  return {
    alternative_index: null,
    open: false
  };
}