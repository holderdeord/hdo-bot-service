import React from 'react';
import PropTypes from 'prop-types';
import { ManuscriptTypeEnum } from "../utils/enums";
import ManuscriptItemForm from "./ManuscriptItemForm";

const ManuscriptForm = ({
                          manuscript,
                          addManuscriptItem,
                          changeManuscriptItemProperty,
                          changeManuscriptProperty,
                          deleteManuscriptItem,
                          onSubmit
                        }) => {
  return (
    <div className="row">
      <div className="col-md-6">
        <form onSubmit={event => onSubmit(event)}>
          <div className="form-group">
            <label htmlFor="name">Name</label>
            <input className="form-control" type="text" id="name" name="name"
                   value={manuscript.name}
                   onChange={(event) => changeManuscriptProperty(event, 'name')}/>
          </div>
          <div className="form-group">
            <label htmlFor="type">Category</label>
            <select className="form-control" id="type" name="type"
                    value={manuscript.type}
                    onChange={(event) => changeManuscriptProperty(event, 'type')}>
              {Object.keys(ManuscriptTypeEnum).map(key => (
                <option key={key} value={ManuscriptTypeEnum[ key ].key}>{ManuscriptTypeEnum[ key ].text}</option>
              ))}
            </select>
          </div>
          <div className="well">
            {manuscript.items.map(item => (
              <ManuscriptItemForm key={item.order}
                                  item={item}
                                  manuscript={manuscript}
                                  changeManuscriptItemProperty={changeManuscriptItemProperty}
                                  deleteManuscriptItem={deleteManuscriptItem}/>
            ))}
            <button className="btn btn-link" type="button"
                    onClick={() => addManuscriptItem()}>
              Add item
            </button>
          </div>
          <button type="submit" className="btn btn-default">Submit</button>
        </form>
      </div>
      <div className="col-md-6">Preview</div>
    </div>
  );
};

ManuscriptForm.propTypes = {
  manuscript: PropTypes.shape({
    name: PropTypes.string.isRequired,
    type: PropTypes.string.isRequired,
    items: PropTypes.arrayOf(PropTypes.shape({
      order: PropTypes.number.isRequired,
      text: PropTypes.string.isRequired,
      type: PropTypes.string.isRequired
    }))
  }),
  addManuscriptItem: PropTypes.func.isRequired,
  changeManuscriptItemProperty: PropTypes.func.isRequired,
  changeManuscriptProperty: PropTypes.func.isRequired,
  deleteManuscriptItem: PropTypes.func.isRequired,
  onSubmit: PropTypes.func.isRequired
};

export default ManuscriptForm;


// class ManuscriptForm extends React.Component {
//   // state = {
//   //   manuscript: new CoreManuscript()
//   // };
//   types = [
//     { pk: 1, name: 'Info', type: ManuscriptTypeEnum.Info },
//     { pk: 2, name: 'ElectoralGuide', type: ManuscriptTypeEnum.ElectoralGuide }
//   ];
//
//   // componentDidMount() {
//   //   console.log('mounting', this.props.manuscript);
//   //   this.setState({
//   //     manuscript: this.props.manuscript
//   //   });
//   // }
//
//   // handleManuscriptNameChange(event) {
//   //   this.props.manuscript.name = event.target.value;
//   //   this.forceUpdate();
//   // }
//   //
//   // handleManuscriptTypeChange(event) {
//   //   this.props.manuscript.type = event.target.value;
//   //   this.forceUpdate();
//   // }
//
//   // addManuscriptItem() {
//   //   this.props.manuscript.addItem();
//   //   this.forceUpdate();
//   // }
//   //
//   // handleManuscriptPropertyChange(event, propertyName) {
//   //   this.props.manuscript[ propertyName ] = event.target.value;
//   //   this.forceUpdate();
//   // }
//   //
//   // handleFormSubmit(event) {
//   //   event.preventDefault();
//   //   this.props.handleSubmit(event);
//   // }
//   //
//   // handleEventPropertyChange(event, item, propertyName) {
//   //   item[ propertyName ] = event.target.value;
//   //   this.forceUpdate();
//   // }
//
//   render() {
//     return (
//       <div>test</div>
//     );
//     // console.log('ManuscriptForm.render', this.props.manuscript);
//     // return (
//     //   <div className="row">
//     //     <div className="col-md-6">
//     //       <form onSubmit={event => this.handleFormSubmit(event)}>
//     //         <div className="form-group">
//     //           <label htmlFor="name">Name</label>
//     //           <input className="form-control" type="text" id="name" name="name"
//     //                  onChange={event => this.handleManuscriptPropertyChange(event, 'name')}
//     //                  value={this.props.manuscript.name}/>
//     //         </div>
//     //         <div className="form-group">
//     //           <label htmlFor="type">Category</label>
//     //           <select className="form-control" id="type" name="type"
//     //                   onChange={event => this.handleManuscriptPropertyChange(event, 'type')}
//     //                   value={this.props.manuscript.type}>
//     //             { this.types.map(this.renderCategoryOption) }
//     //           </select>
//     //         </div>
//     //         <div className="well">
//     //           {this.props.manuscript.items.map(item => this.renderManuscriptItem(item))}
//     //           <button className="btn btn-link" type="button"
//     //                   onClick={event => this.addManuscriptItem(event)}>Add item
//     //           </button>
//     //         </div>
//     //         <button type="submit" className="btn btn-default">Submit</button>
//     //       </form>
//     //     </div>
//     //     <div className="col-md-6">Preview</div>
//     //   </div>
//     // );
//   }
//
//   renderCategoryOption({ pk, name, type }) {
//     return (
//       <option key={pk} value={type}>{name}</option>
//     );
//   }
//
//   renderManuscriptItem(item) {
//     let { order, text, type } = item;
//     return (
//       <div key={order} className="panel panel-default">
//         <div className="panel-heading">
//           Item #{order}
//         </div>
//         <div className="panel-body">
//           <div className="form-group">
//             <label htmlFor={`itemType-${order}`}>Type</label>
//             <select className="form-control" id={`itemType-${order}`} name="itemType"
//                     onChange={event => this.handleEventPropertyChange(event, item, 'type')}
//                     value={type}>
//               <option value="text">Text</option>
//               <option value="button">Button</option>
//             </select>
//           </div>
//           <div className="form-group">
//             <label htmlFor={`itemText-${order}`}>Text</label>
//             <input className="form-control" type="text" id={`itemText-${order}`} name="itemText"
//                    onChange={event => this.handleEventPropertyChange(event, item, 'text')}
//                    defaultValue={text}/>
//           </div>
//           <div className="btn-group" role="group">
//             <button type="button" className="btn btn-default">
//               <span className="glyphicon glyphicon-arrow-up" /> Move up
//             </button>
//             <button type="button" className="btn btn-default">
//               <span className="glyphicon glyphicon-arrow-down" /> Move down
//             </button>
//             <DeleteManuscriptItemButton item={item} manuscript={this.props.manuscript}/>
//           </div>
//         </div>
//       </div>
//     );
//   }
// }
//
// export default ManuscriptForm;
