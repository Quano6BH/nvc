// SPDX-License-Identifier: GPL-3.0

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract FakeBUSD is ERC20{
    constructor() ERC20("Binance USD", "BUSD"){

    }

    function mint(uint256 amount_) external{
        _mint(msg.sender, amount_);
    }
}