import React from 'react';
import { connect } from "react-redux";
import ManuscriptForm from "../components/ManuscriptForm";

const mapStateToProps = (state, {match}) => {
  console.log('test', match.params.manuscriptId);
  return {
    manuscript: {
      name: 'Test',
      type: 'info',
      items: []
    }
  };
};

const mapDispatchToProps = (dispatch, ownProps) => {
  // let manuscript = addManuscript();
  // dispatch(manuscript);
  // dispatch(addManuscriptItem(manuscript.id));
  return {
    addManuscriptItem: () => {
      // dispatch(addManuscriptItem(manuscript.id));
    },
    changeManuscriptProperty: (event, propertyName) => {
      // dispatch(changeManuscriptProperty(manuscript.id, propertyName, event.target.value));
    },
    changeManuscriptItemProperty: (event, order, propertyName) => {
      // dispatch(changeManuscriptItemProperty(manuscript.id, order, propertyName, event.target.value));
    },
    deleteManuscriptItem: (order) => {
      // dispatch(deleteManuscriptItem(manuscript.id, order));
    },
    onSubmit: (event, manuscript) => {
      event.preventDefault();
      // dispatch(postManuscript(manuscript));
      // const payload = {
      //   name: manuscript.name,
      //   items: manuscript.items.map(item => {
      //     return {
      //       type: item.type,
      //       order: item.order,
      //       text: item.text,
      //       buttonText: ''
      //     };
      //   })
      // };
      // return fetch(getManuscriptApiUrl(), {
      //   method: 'POST',
      //   body: JSON.stringify(payload),
      //   headers: new Headers({
      //     'Content-Type': 'application/json'
      //   })
      // })
      //   .then(response => response.json())
      //   .then(createdManuscript => {
      //     console.log('createdManuscript', createdManuscript, ownProps);
      //   })
      //   .catch(response => dispatch(postManuscript(manuscript, response)));
    }
  }
};

const EditManuscript = connect(
  mapStateToProps,
  mapDispatchToProps
)(ManuscriptForm);

export default EditManuscript;




// import ManuscriptForm from "./ManuscriptForm";
// import InfoManuscript from "../manuscripts/InfoManuscript";
// import ManuscriptFactory from "../manuscripts/ManuscriptFactory";
//
// export default class EditManuscriptComponent extends React.Component {
//   state = {
//     manuscript: new InfoManuscript()
//   };
//
//   constructor(props) {
//     super(props);
//     this.manuscriptId = props.match.params.manuscriptId;
//     this.manuscriptFactory = new ManuscriptFactory();
//   }
//
//   componentDidMount() {
//     fetch(`http://localhost:8000/api/manuscripts/${this.manuscriptId}`)
//       .then(response => response.json())
//       .then(manuscriptData => this.setState({
//         manuscript: this.manuscriptFactory.loadManuscript(manuscriptData)
//       }));
//   }
//
//   handleSubmit(event) {
//     console.log('submitting', this.state.manuscript);
//   }
//
//   render() {
//     console.log('EditManuscriptComponent.render', this.state.manuscript);
//     return <ManuscriptForm manuscript={this.state.manuscript}
//                            handleSubmit={event => this.handleSubmit(event)}/>;
//   }
// }
