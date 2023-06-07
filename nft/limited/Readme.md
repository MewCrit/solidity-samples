## CODE REVIEW

```
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/utils/Counters.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";

contract MyNFT is ERC721URIStorage, Ownable {
    using Counters for Counters.Counter;

    Counters.Counter private _tokenIds;

    // Define a structure to hold Pokémon data
    struct Pokemon {
        string name;
        uint maxSupply;
        uint currentSupply;
    }

    // Map the Pokémon ID to its data
    mapping(uint => Pokemon) private _pokemon;

    constructor() ERC721("MyNFT", "NFT") {}

    // Add a new Pokémon type to the contract
    function addPokemon(uint pokemonId, string memory name, uint maxSupply) public onlyOwner {
        _pokemon[pokemonId] = Pokemon(name, maxSupply, 0);
    }

    // Mint a new Pokémon token
    function mintPokemon(uint pokemonId, address recipient, string memory tokenURI) public onlyOwner returns (uint256) {
        require(_pokemon[pokemonId].currentSupply < _pokemon[pokemonId].maxSupply, "Max supply reached for this Pokemon");
        
        _tokenIds.increment();

        uint256 newItemId = _tokenIds.current();
        _mint(recipient, newItemId);
        _setTokenURI(newItemId, tokenURI);
        
        // Increment the supply of the given Pokémon type
        _pokemon[pokemonId].currentSupply += 1;

        return newItemId;
    }
}


```


A struct Pokemon has been defined to hold each Pokémon's name, maximum supply, and current supply.

A mapping _pokemon has been created to map each Pokémon ID to its data.

A function addPokemon has been added that allows the owner of the contract to add a new Pokémon type.

The mintNFT function has been renamed to mintPokemon and modified to take a pokemonId. This function first checks if the current 
supply of the specified Pokémon is less than its max supply before minting a new token. After minting the token, it increments the 
current supply of the given Pokémon type.
