import React from 'react';
import { Link } from "react-router-dom";

const ManuscriptTable = ({manuscripts}) => (
  <div>
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
      { manuscripts.map(renderManuscript) }
      </tbody>
    </table>
  </div>
);

const renderManuscript = ({ pk, name, category }) => (
  <tr key={ `manuscript-${pk}` }>
    <td>{ pk }</td>
    <td>
      <Link to={`/edit/${ pk }`}>{ name }</Link>
    </td>
    <td>{ category }</td>
  </tr>
);

export default ManuscriptTable;
