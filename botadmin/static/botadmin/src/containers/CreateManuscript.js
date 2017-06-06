import React from 'react';
import ManuscriptForm from "../components/ManuscriptForm";
import { connect } from "react-redux";
import {
  addManuscript, addManuscriptItem, changeManuscriptItemProperty, changeManuscriptProperty,
  deleteManuscriptItem, postManuscript
} from "../actions/manuscripts";

const mapStateToProps = (state) => {
  return {
    manuscript: state.manuscripts.length > 0 ? state.manuscripts[state.manuscripts.length - 1] : {
      name: '',
      type: 'info',
      items: []
    }
  };
};

const mapDispatchToProps = (dispatch) => {
  let manuscript = addManuscript();
  dispatch(manuscript);
  dispatch(addManuscriptItem(manuscript.id));
  return {
    addManuscriptItem: () => {
      dispatch(addManuscriptItem(manuscript.id));
    },
    changeManuscriptProperty: (event, propertyName) => {
      dispatch(changeManuscriptProperty(manuscript.id, propertyName, event.target.value));
    },
    changeManuscriptItemProperty: (event, order, propertyName) => {
      dispatch(changeManuscriptItemProperty(manuscript.id, order, propertyName, event.target.value));
    },
    deleteManuscriptItem: (order) => {
      dispatch(deleteManuscriptItem(manuscript.id, order));
    },
    onSubmit: (event) => {
      event.preventDefault();
      dispatch(postManuscript(manuscript.id));
    }
  }
};

const CreateManuscript = connect(
  mapStateToProps,
  mapDispatchToProps
)(ManuscriptForm);

export default CreateManuscript;


// export default class CreateManuscript extends React.Component {
//   // componentDidMount() {
//   //   fetch('http://localhost:8000/api/categories/')
//   //     .then(response => response.json())
//   //     .then(categories => this.setState({ categories }));
//   // }
//
//   // handleSubmit(event) {
//   //   console.log('submitting', this.state.manuscript);
//   // }
//
//   render() {
//     return connect()(ManuscriptForm);
//   }
// }
