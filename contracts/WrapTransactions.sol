//SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.4;

import "./Ownable.sol";

interface IERC20 {
    function transfer(address to, uint256 value) external returns (bool);

    function transferFrom(
        address from,
        address to,
        uint256 value
    ) external returns (bool);
}

contract WrapTransactions is Ownable{
    event TransferFailed(address to, uint256 value);

    address public constant BUSD_CONTRACT =
        0x78867BbEeF44f2326bF8DDd1941a4439382EF2A7;

    constructor() {}

    function scatterEther(
        address[] memory recipients,
        uint256[] memory values,
        bool revertOnfail
    ) external payable {
        uint256 totalSuccess = 0;
        for (uint256 i = 0; i < recipients.length; i++) {
            (bool success, ) = recipients[i].call{value: values[i], gas: 3500}(
                ""
            );
            if (revertOnfail) require(success, "One of the transfers failed");
            else if (success == false) {
                emit TransferFailed(recipients[i], values[i]);
            }
            if (success) totalSuccess++;
        }

        require(totalSuccess >= 1, "all transfers failed");
        returnExtraEth();
    }

    function scatterBUSD(
        address[] memory recipients,
        uint256[] memory values,
        bool revertOnfail
    ) external onlyOwner {
        uint256 totalSuccess = 0;

        for (uint256 i = 0; i < recipients.length; i++) {
            (bool success, bytes memory returnData) = address(
                IERC20(BUSD_CONTRACT)
            ).call(
                    abi.encodePacked(
                        IERC20(BUSD_CONTRACT).transferFrom.selector,
                        abi.encode(msg.sender, recipients[i], values[i])
                    )
                );

            if (success) {
                bool decoded = abi.decode(returnData, (bool));
                if (revertOnfail == true)
                    require(decoded, "One of the transfers failed");
                else if (decoded == false)
                    emit TransferFailed(recipients[i], values[i]);
                if (decoded) totalSuccess++;
            } else if (success == false) {
                if (revertOnfail == true)
                    require(false, "One of the transfers failed");
                else emit TransferFailed(recipients[i], values[i]);
            }
        }
        require(totalSuccess >= 1, "all transfers failed");
    }

    function returnExtraEth() internal {
        uint256 balance = address(this).balance;
        if (balance > 0) {
            payable(msg.sender).transfer(balance);
        }
    }

}
