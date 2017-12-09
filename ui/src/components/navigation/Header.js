import React, {Component} from 'react';
import {Link} from 'react-router-dom';
import Auth from '../../utils/auth'
import {withRouter} from 'react-router-dom'

import {
  Nav,
  NavbarToggler,
  NavItem,
} from 'reactstrap';

class Header extends Component {

  constructor(props) {
    super(props);
  }

  sidebarToggle(e) {
    e.preventDefault();
    document.body.classList.toggle('sidebar-hidden');
  }

  sidebarMinimize(e) {
    e.preventDefault();
    document.body.classList.toggle('sidebar-minimized');
  }

  mobileSidebarToggle(e) {
    e.preventDefault();
    document.body.classList.toggle('sidebar-mobile-show');
  }

  logout(e) {
      e.preventDefault();
      Auth.deAuthenticateUser();
      this.props.history.push("/login");
  }

  render() {
    return (
      <header className="app-header navbar">
        <NavbarToggler className="d-lg-none" onClick={this.mobileSidebarToggle}>
          <span className="navbar-toggler-icon"></span>
        </NavbarToggler>
        <NavbarToggler className="d-md-down-none" onClick={this.sidebarToggle}>
          <span className="navbar-toggler-icon"></span>
        </NavbarToggler>
        <Nav className="" navbar>
          <NavItem className="px-3">
            <Link to="/main-page">Rooms</Link>
          </NavItem>
          <NavItem className="px-3">
            <Link to="/ifttt-list">Rules</Link>
          </NavItem>
          <NavItem className="px-3">
            <Link to="" onClick={this.logout.bind(this)}>Logout</Link>
          </NavItem>
        </Nav>
        <Nav className="ml-auto" navbar>
        </Nav>
      </header>
    );
  }
}

export default Header;
