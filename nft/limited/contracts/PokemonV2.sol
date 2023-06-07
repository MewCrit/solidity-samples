// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/utils/Counters.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";

contract PokemonV2 is ERC721URIStorage, Ownable {
    using Counters for Counters.Counter;

    Counters.Counter private _tokenIds;

    struct Pokemon {
        string name;
        uint maxSupply;
        uint currentSupply;
    }

    mapping(uint => Pokemon) private _pokemon;

    constructor() ERC721("D POKEMON NFTS", "DPKMN") {}

    function addPokemon(uint pokemonId, string memory name, uint maxSupply) public onlyOwner {
        _pokemon[pokemonId] = Pokemon(name, maxSupply, 0);
    }

    function mintPokemon(uint pokemonId, address recipient, string memory tokenURI) public onlyOwner returns (uint256) {
        require(_pokemon[pokemonId].currentSupply < _pokemon[pokemonId].maxSupply, "Max supply reached for this Pokemon");
        
        _tokenIds.increment();

        uint256 newItemId = _tokenIds.current();
        _mint(recipient, newItemId);
        _setTokenURI(newItemId, tokenURI);
        
        _pokemon[pokemonId].currentSupply += 1;

        return newItemId;
    }
}
