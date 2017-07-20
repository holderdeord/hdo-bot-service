import React from 'react';
import _ from 'lodash';
import { Button } from "react-bootstrap";

export default props =>
  <li className="list-group-item">
    <span className="badge">
      {props.result._source.promisor_name},{' '}
      {props.result._source.parliament_period_name}
    </span>

    <span dangerouslySetInnerHTML={{
      __html: _.get(
        props.result,
        'highlight.body',
        props.result._source.body
      )
    }}
    />&nbsp;
    <Button bsSize="xsmall" onClick={() => alert('test')}>Legg til</Button>
  </li>;