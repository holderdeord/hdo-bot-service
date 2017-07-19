import React from 'react';

const ManuscriptAlternativeForm = ({
                                     alternative,
                                     changeManuscriptAlternativeProperty,
                                     index
                                   }) => {
  return (
    <div className="panel panel-default">
      <div className="panel-heading">
        {alternative.text}
      </div>
      <div className="panel-body">
        <div className="form-group">
          <label>Tekst</label>
          <input className="form-control"
                 onSelect={(event) => changeManuscriptAlternativeProperty(event, index, 'text')}
                 defaultValue={alternative.text}/>
        </div>
        <div className="form-group">
          <label>Partier</label>
          <p>{alternative.parties.join(', ')}</p>
        </div>
      </div>
    </div>
  );
};

export default ManuscriptAlternativeForm;