import React, { Component } from "react";
import './App.css';
import { v4 as uuidv4 } from 'uuid';


class Main extends Component {

   
    constructor(props) {
        super(props)
    }

    render() {
        return(
            <div id="content">
                    <br/>
                    <form onSubmit={(event) => {

                        event.preventDefault()

                        const fullName = this.fullName.value
                        const residentID = uuidv4()
                        const homeAddress = this.homeAddress.value
                        const nationality = this.nationality.value
                        const natureOfResidency = this.natureOfResidency.value
                        const image = this.image.value
                        const signature = this.signature.value

                        this.props.createID(fullName, residentID, homeAddress, nationality, natureOfResidency, image, signature)
                    }}>

                    <div className="form-group mr-sm-2">
                        <input id="fullName" type="text" ref={(i) => {this.fullName = i}} className="form-control" placeholder="Fullname" required />
                    </div>
                    <div className="form-group mr-sm-2">
                        <input id="homeAddress" type="text" ref={(i) => {this.homeAddress = i }} className="form-control" placeholder="Home address" required  />
                    </div>
                    <div className="form-group mr-sm-2">
                        <input id="nationality" type="text" ref={(i) => {this.nationality = i}} className="form-control" placeholder="Nationality" required  />
                    </div>
                    <div className="form-group mr-sm-2">
                        <input id="natureOfResidency" type="text" ref={(i) => {this.natureOfResidency = i}} className="form-control" placeholder="Nature Of Residency" required  />
                    </div>
                    <div className="form-group mr-sm-2">
                        <input id="image" type="text" ref={(i) => {this.image = i}} className="form-control" placeholder="Image" required  />
                    </div>
                    <div className="form-group mr-sm-2">
                        <input id="signature" type="text" ref={(i) => {this.signature = i}} className="form-control" placeholder="Signature" required  />
                    </div>
                    <button type="submit" className="btn btn-primary">Create ID</button>

                </form>





            </div>
        )
    }

}


export default Main 