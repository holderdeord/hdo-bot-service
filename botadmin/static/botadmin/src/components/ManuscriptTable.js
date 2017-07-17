import React from 'react';
import PropTypes from 'prop-types';
import { Link } from "react-router-dom";
import * as moment from 'moment';

const ManuscriptTable = ({
                           manuscripts,
                           deleteManuscript,
                           sortManuscripts
                         }) => (
  <div>
    <ul className="nav nav-pills">
      <li role="presentation">
        <Link to="/create">Create new manuscript</Link>
      </li>
    </ul>
    <table className="table table-striped">
      <thead>
      <tr>
        <th>
          <a onClick={() => sortManuscripts('pk')}>#</a>
        </th>
        <th>
          <a onClick={() => sortManuscripts('name')}>Name</a>
        </th>
        <th>
          <a onClick={() => sortManuscripts('type')}>Type</a>
        </th>
        <th>
          <a onClick={() => sortManuscripts('category')}>Category</a>
        </th>
        <th>
          <a onClick={() => sortManuscripts('hdo_category')}>HDO Category</a>
        </th>
        <th># Items</th>
        <th>Last Updated</th>
        <th>Actions</th>
      </tr>
      </thead>
      <tbody>
      { manuscripts.map(({ pk, name, type, category, hdo_category, items, updated }, index) => (
        <tr key={ `manuscript-${index}` }>
          <td>{ pk }</td>
          <td>
            <Link to={`/edit/${ pk }`}>{ name }</Link>
          </td>
          <td>{type}</td>
          <td>{category}</td>
          <td>{hdo_category}</td>
          <td>{items.length}</td>
          <td>{moment().from(updated)}</td>
          <td>
            <div className="btn-group btn-group-xs" role="group">
              <button className="btn btn-danger" type="button" onClick={() => deleteManuscript(pk)}>
                <span className="glyphicon glyphicon-trash"/> Delete
              </button>
            </div>
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
