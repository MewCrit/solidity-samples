// SPDX-License-Identifier:MIT
pragma solidity >=0.6.0 <0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract MyToken is ERC20 {
    constructor(uint256 initialSupply) ERC20("Tixers", "TIX") {
        _mint(msg.sender, initialSupply);
    }
}
