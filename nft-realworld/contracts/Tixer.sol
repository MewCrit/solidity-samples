// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";

contract Tixer is ERC721URIStorage {

    address public owner;
    uint256 public totalSupply;

    mapping(string => Movie) public movies;
    // Movie ID => (Seat => Address)
    mapping(string => mapping(string => address)) public seat;
    // MovieID => Available seats
    mapping(string => string[])  public seats;

    struct Movie {
        string id;
        string image;
        string movieName;
        string genre;
        uint256 price;
        uint256 tickets;
        uint256 maxTickets;
        uint256 cinemaArea;
        string remarks;
        string time;
        string location;
        string lftrbRatings;
    }

    modifier ownerOnly() {
        require(msg.sender == owner, "Only the owner can perform this action");
        _;
    }

    constructor(string memory _tokenName, string memory _tokenSymbol) ERC721(_tokenName, _tokenSymbol) {
        owner = msg.sender;
    }

    event MovieAdded(string id, string movieName, string message);

    function mintTicket(string calldata _seat, string memory _movieID, string calldata _tokenURI) public payable {
        
        require(movies[_movieID].tickets > 0, "Tickets are soldout");       
        require(msg.value >= movies[_movieID].price, "Not enough cash");

        movies[_movieID].tickets -= 1;

        totalSupply += 1;

        seat[_movieID][_seat] = msg.sender;
        seats[_movieID].push(_seat);
                
        _mint(msg.sender, totalSupply);
        _setTokenURI(totalSupply, _tokenURI);
    }


    function addMovies(string memory _id, 
        string memory _image, 
        string memory _movieName,  
        string memory _genre , 
        uint256 _price, 
        uint256 _tickets, 
        uint256 _maxTickets, 
        uint256 _cinemaArea, 
        string memory _remarks, 
        string memory _time, 
        string memory _location, 
        string memory _lftrbRatings) public ownerOnly {
       
        movies[_id] = Movie(
            _id,
            _image,
            _movieName,
            _genre,
            _price,
            _tickets,
            _maxTickets,
            _cinemaArea,
            _remarks,
            _time,
            _location,
            _lftrbRatings
        );

        emit MovieAdded(movies[_id].id, movies[_id].movieName, "Movie added to mappings");
    }

    function getMovies(string memory _id) public view returns(Movie memory) {
        return movies[_id];    
    }

    function getSeats(string memory _id) public view returns (string[] memory) {
        return seats[_id];
    }

  

  
}