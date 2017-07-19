import React from 'react';
import { Button } from "react-bootstrap";

const ManuscriptAlternativeForm = ({
                                     alternative,
                                     changeManuscriptAlternativeProperty,
                                     index,
                                     openPromisesModal
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
          <label>Løfter</label>
          <ul>
            {alternative.promises.map(promise => (
              <li key={`alternative-promise-${index}-${promise.pk}`}>{promise.body} ({promise.promisor_name})</li>
            ))}
          </ul>
          <Button onClick={() => openPromisesModal(index)}>Legg til løfte</Button>
        </div>
        <div className="form-group">
          <label>Partier</label>
          <p>{[ ...new Set(alternative.parties) ].join(', ')}</p>
        </div>
      </div>
    </div>
  );
};

export default ManuscriptAlternativeForm;