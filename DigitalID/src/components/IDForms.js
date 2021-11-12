import React, { Component } from 'react';
import logo from '../logo.jpg';
import './App.css';
import DigitalID from '../abis/DigitalID.json'
import Web3 from 'web3';
import Navbar from './Navbar'
import Main from './Main'



class IDForms extends Component {


    render() {

        return(
            <div>
                <table className="table">
                    <thead>
                        <tr>
                            <th>Image</th>
                            <th>Owner Address</th>
                            <th>Fullname</th>
                            <th>ResidentID</th>
                            <th>Home Address</th>
                            <th>Nationality</th>
                            <th>Nature Of Residency</th>
                            <th>Signature</th>
                        </tr>
                    </thead>
                    <tbody>
                                {
                                    this.props.ids.map((id, key) => {
                                        
                                        return(
                                            <tr key={key}>
                                                <td><img src={id.image} height="90" width="90"></img></td>
                                                <td>{id.ownerId}</td>
                                                <td>{id.fullName}</td>
                                                <td>{id.residentID}</td>
                                                <td>{id.homeAddress}</td>
                                                <td>{id.nationality}</td>
                                                <td>{id.natureOfResidency}</td>
                                                <td><img src={id.signature} height="90" width="90"></img></td>
                                            </tr>
                                        )
                                    })
                                }
                        
                    </tbody>
                </table> 
            </div>
        )
    }

}


export default IDForms