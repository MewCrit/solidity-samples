import React, { Component } from 'react';
import logo from '../logo.jpg';
import './App.css';
import DigitalID from '../abis/DigitalID.json'
import Web3 from 'web3';
import Navbar from './Navbar'
import Main from './Main'
import IDForms from './IDForms'



class App extends Component {

async componentWillMount() {
  
   await this.loadWeb3()
   await this.loadData()
}

constructor(props) {

  super(props)
    this.state = {
      account : '',
      idCount: 0,
      ids : [],
      loading: true
    }

    this.createID = this.createID.bind(this)
}

async loadWeb3() {
    if (window.ethereum) {
        window.web3 = new Web3(window.ethereum)
        await window.ethereum.enable()
    } 
    else if (window.web3) {
      window.web3 = new Web3(window.web3.currentProvider)
    } else {
        alert('Install meta mask!')
    }
}

async loadData() {

    const web3 = window.web3

    const accounts = await web3.eth.getAccounts()
    this.setState({
      account : accounts[0]
    })

    const networkId = await web3.eth.net.getId()
    const networkData= DigitalID.networks[networkId]
    
    if(networkData) {
      const digitalID = new web3.eth.Contract(DigitalID.abi, networkData.address)
       this.setState({digitalID})

      const countDigitalId = await digitalID.methods.countIdApplication().call()
      this.setState({ countDigitalId })
     
      for (var i = 1; i <= countDigitalId; i++) {
        const id = await digitalID.methods.idForms(i).call()
        this.setState({
          ids: [...this.state.ids, id]
        })
      }
      console.log(this.state.ids)
        this.setState({
          loading : false
        })
    } else {
      alert('Digital id smart contract not deployed')
    }
}


createID(fullname, residentID, homeAddress, nationality, natureOfResidency, image,  signature) {
  this.state.digitalID.methods.createDigitalId(fullname, residentID, homeAddress, nationality, natureOfResidency, image,  signature)
      .send({from: this.state.account})
      .once('receipt', (receipt) => {
        this.setState({loading: false})
      })
}


  render() {
    return (
      <div>
        <Navbar appname={'Online Digital ID'} account={this.state.account}></Navbar>
        <div className="container-fluid mt-5">
          <div className="row">
            <main role="main" className="col-lg-12 text-center">
              <div className="content mr-auto ml-auto">
                <a href="#"  target="_blank"  rel="noopener noreferrer">
                  <img src={logo} className="App-logo" alt="logo" height="150" width="150"/>
                </a>
              <br/>
              <div className="row">
                <div className="col-md-4">

                <div className="card" >
                    <div className="card-header">
                      Create Digital ID
                    </div>
                    <div className="card-body">
                         {
                            this.state.loading 
                            ? <div id="loader" className="text-center">
                                <p className="text-center">Loading....</p>
                              </div>
                            : <Main createID={this.createID} />
                          }
                      </div>
                  </div>
                   
                </div>
                <div className="col-md-8">
                    <div className="card">
                          <div className="card-header">
                            List of registered users
                          </div>
                          <div className="card-body">
                            <IDForms ids={this.state.ids} />
                          </div>
                        </div>
                </div>
              </div>

              </div>
            </main>
          </div>
        </div>
      </div>
    );
  }
}

export default App;