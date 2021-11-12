pragma solidity 0.6.12;

contract DigitalID {


      uint public countIdApplication = 0;
      mapping(uint => DigitalIdForm) public  idForms;

      struct DigitalIdForm {
            address ownerId;
            string fullName;
            string residentID;
            string homeAddress;
            string nationality;
            string natureOfResidency;
            string image;
            string signature; 
    }
 
    event DigitalIdCreated(
            address ownerId,
            string fullName,
            string residentID,
            string homeAddress,
            string nationality,
            string natureOfResidency,
            string image,
            string signature);


    function createDigitalId(string memory _fullname, string memory _residentID, string memory _homeAddress,
                             string memory _nationality, string memory _natureOfResidency,
                             string memory _image, string memory _signature) public {
        
       uint id = countIdApplication ++;
       
       address contractAddress = msg.sender;
        
       DigitalIdForm storage digitalIdForm = idForms[id];
       digitalIdForm.ownerId = contractAddress;
       digitalIdForm.fullName = _fullname;
       digitalIdForm.residentID = _residentID;
       digitalIdForm.homeAddress = _homeAddress;
       digitalIdForm.nationality = _nationality;
       digitalIdForm.natureOfResidency = _natureOfResidency;
       digitalIdForm.image = _image;
       digitalIdForm.signature = _signature;


       emit DigitalIdCreated(contractAddress, _fullname, _residentID, _homeAddress, _nationality, _natureOfResidency, _image,_signature );

    }




}