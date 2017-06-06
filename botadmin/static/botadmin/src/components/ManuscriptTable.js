import React from 'react';
import PropTypes from 'prop-types';
import { Link } from "react-router-dom";

const ManuscriptTable = ({ manuscripts, deleteManuscript }) => (
  <div>
    <Link to="/create">Create new manuscript</Link>
    <table className="table table-striped">
      <thead>
      <tr>
        <th>#</th>
        <th>Name</th>
        <th>Actions</th>
      </tr>
      </thead>
      <tbody>
      { manuscripts.map(({ pk, name, category }) => (
        <tr key={ `manuscript-${pk}` }>
          <td>{ pk }</td>
          <td>
            <Link to={`/edit/${ pk }`}>{ name }</Link>
          </td>
          <td>
            <button className="btn btn-default" type="button" onClick={() => deleteManuscript(pk)}>
              <span className="glyphicon glyphicon-trash"></span>
            </button>
          </td>
        </tr>
      )) }
      </tbody>
    </table>
  </div>
);

ManuscriptTable.propTypes = {
  manuscripts: PropTypes.arrayOf(PropTypes.shape({
    pk: PropTypes.number.isRequired,
    name: PropTypes.string.isRequired
  })),
  deleteManuscript: PropTypes.func.isRequired
};

export default ManuscriptTable;
