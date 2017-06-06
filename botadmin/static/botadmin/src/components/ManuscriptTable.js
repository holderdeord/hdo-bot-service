import React from 'react';
import { Link } from "react-router-dom";

class ManuscriptTable extends React.Component {
  // constructor(props) {
  //   super(props);
  // }

  render() {
    return <div>
      <Link to="/create">Create new manuscript</Link>
      <table className="table table-striped">
        <thead>
        <tr>
          <th>#</th>
          <th>Name</th>
          <th>Category</th>
        </tr>
        </thead>
        <tbody>
        { this.props.manuscripts.map(this.renderManuscript) }
        </tbody>
      </table>
    </div>;
  }

  renderManuscript({ pk, name, category }) {
    return <tr key={ pk }>
      <td>{ pk }</td>
      <td>
        <Link to={`/view/${ pk }`}>{ name }</Link>
      </td>
      <td>{ category }</td>
    </tr>;
  }
}

export default ManuscriptTable;
