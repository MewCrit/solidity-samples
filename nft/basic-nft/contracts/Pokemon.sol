// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract Pokemon is ERC721URIStorage, Ownable {

    constructor() ERC721("Pokemon nft", "PKMN") {

    }

    function mint(address _to, uint256 _tokenId, string calldata _tokenURI) external onlyOwner {
        _mint(_to, _tokenId);
        _setTokenURI(_tokenId, _tokenURI);

    }


}