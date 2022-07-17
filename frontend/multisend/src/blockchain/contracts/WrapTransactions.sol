//SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.4;

import "./Ownable.sol";

interface IERC20 {
    function transfer(address to, uint256 value) external returns (bool);

    function transferFrom(
        address from,
        address to,
        uint256 value
    ) external returns (bool, bytes memory);
}

contract WrapTransactions is Ownable {
    event TransferFailed(address to, uint256 value);

    function scatterTokens(
        IERC20 token,
        address[] memory recipients,
        uint256[] memory values,
        bool revertOnfail
    ) external onlyOwner {
        uint256 totalSuccess = 0;

        for (uint256 i = 0; i < recipients.length; i++) {
            (bool success, bytes memory returnData) = token.transferFrom(msg.sender, recipients[i], values[i]);


            if (success) {
                bool decoded = abi.decode(returnData, (bool));
                require(revertOnfail && decoded, "One of the transfers failed");
                    
                if (!decoded)
                    emit TransferFailed(recipients[i], values[i]);
                else 
                    totalSuccess++;

            } else {
                
                require(revertOnfail, "One of the transfers failed");

                emit TransferFailed(recipients[i], values[i]);
            }
        }

        require(totalSuccess >= 1, "all transfers failed");
    }
}