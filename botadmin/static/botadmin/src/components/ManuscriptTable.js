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
        <th># Items</th>
        <th>Last Updated</th>
        <th>Actions</th>
      </tr>
      </thead>
      <tbody>
      { manuscripts.map(({ pk, name, items, updated }, index) => (
        <tr key={ `manuscript-${index}` }>
          <td>{ pk }</td>
          <td>
            <Link to={`/edit/${ pk }`}>{ name }</Link>
          </td>
          <td>{items.length}</td>
          <td>{updated}</td>
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
    // pk: PropTypes.number.isRequired,
    name: PropTypes.string.isRequired
  })),
  deleteManuscript: PropTypes.func.isRequired
};

export default ManuscriptTable;
