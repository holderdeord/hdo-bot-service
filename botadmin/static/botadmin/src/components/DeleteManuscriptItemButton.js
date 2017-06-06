import React  from "react";

const DeleteManuscriptItemButton = ({manuscript, onClick}) => {
  return manuscript.items.length > 1 ? (
    <button type="button" className="btn btn-danger" onClick={() => onClick()}>
      <span className="glyphicon glyphicon-remove"/> Delete
    </button>
  ) : null;
};

export default DeleteManuscriptItemButton;

// export default class DeleteManuscriptItemButton extends Component {
//   render() {
//     return this.props.manuscript.hasMultipleItems() ? (
//       <button type="button" className="btn btn-danger" onClick={() => this.removeItem()}>
//         <span className="glyphicon glyphicon-remove"/> Delete
//       </button>
//     ) : null;
//   }
//
//   removeItem() {
//     this.props.manuscript.removeItem(this.props.item);
//   }
// }