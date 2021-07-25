# Basic ERC20

## Run this on Ethereum Remix https://remix.ethereum.org/   


Copy paste this on Ethereum Remix
```
pragma solidity >=0.7.0 <0.9.0;
 
import "github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/ERC20.sol"; 
import "github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/extensions/ERC20Burnable.sol";
 
contract Loogle is ERC20, ERC20Burnable  {
    
    // Crypto
    constructor() ERC20("Loogle", "LGL") {
        _mint(msg.sender, 10000000);
    }
    
}

```
