import * as React from "react";
import { Nav, Navbar } from "react-bootstrap";
import { Link } from "react-router-dom";
import './Header.css';
import NavItem from "./NavItem";

const Header = () => (
  <Navbar className="main-navigation">
    <Navbar.Header>
      <Navbar.Brand>
        <Link className="navbar-brand" to="/">Holder de ord</Link>
      </Navbar.Brand>
      <Nav>
        <NavItem activeClassName="active" to="/">Manuscripts</NavItem>
      </Nav>
    </Navbar.Header>
  </Navbar>
);

export default Header;