import React from 'react';

class ManuscriptTable extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    return <table>
      <thead>
      <tr>
        <th>PK</th>
        <th>Name</th>
        <th>Category</th>
      </tr>
      </thead>
      <tbody>
        { this.props.manuscripts.map(this.renderManuscript) }
      </tbody>
    </table>;
  }

  renderManuscript({ pk, name, category }) {
    return <tr key="{ pk }">
      <td>{ pk }</td>
      <td>{ name }</td>
      <td>{ category }</td>
    </tr>;
  }
}

export default ManuscriptTable;
