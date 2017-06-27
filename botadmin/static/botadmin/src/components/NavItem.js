import * as React from "react";
import { Link, Route } from "react-router-dom";

class NavItem extends React.Component {
  render() {
    const { to, exact, children, activeClassName } = this.props;
    return (
      <Route path={to} exact={exact} children={({ match }) => (
        <li className={match.isExact ? activeClassName : null}>
          <Link to={to}>{children}</Link>
        </li>
      )}/>
    );
  }
}

export default NavItem;
