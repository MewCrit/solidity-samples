
import React, { Component } from 'react';
import { ethers } from 'ethers'
import './App.css';

class Navbar extends Component {

    constructor (props) {

        super(props)
        this.state = {

        }
    }



    render() {
      return(
        <nav className="navbar navbar-dark fixed-top bg-dark flex-md-nowrap p-0 shadow">
        <a className="navbar-brand col-sm-3 col-md-2 mr-0"   rel="noopener noreferrer" >
          {this.props.appname}

        
        </a>
        <ul className="navbar-nav px-3">
          <li className="nav-item text-nowrap d-none d-sm-none d-sm-block">
            <small className="text-white">My Wallet Address : <span id="account">{this.props.account}</span></small>
          </li>
        </ul>
      </nav>
      )
    }


}


export default Navbar;

