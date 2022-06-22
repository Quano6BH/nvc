/**
 *Submitted for verification at BscScan.com on 2021-10-30
 */

//SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.6;

interface IERC20 {
    function transfer(address to, uint256 value) external returns (bool);

    function transferFrom(
        address from,
        address to,
        uint256 value
    ) external returns (bool);
}

contract WrapTransactions {
    event TransferFailed(address to, uint256 value);

    address public owner;
    address public constant BUSD_CONTRACT =
        0x78867BbEeF44f2326bF8DDd1941a4439382EF2A7;

    constructor() {
        owner = msg.sender;
    }

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
    ) external {
        uint256 totalSuccess = 0;

        for (uint256 i = 0; i < recipients.length; i++) {
            // (bool success, bytes memory returnData) = address(
            //     IERC20(BUSD_CONTRACT)
            // ).call(
            //         abi.encodePacked(
            //             IERC20(BUSD_CONTRACT).transferFrom.selector,
            //             abi.encode(msg.sender, recipients[i], values[i])
            //         )
            //     );
            bool success = IERC20 (BUSD_CONTRACT).transferFrom(msg.sender,recipients[i],values[i]);

            if (success) {
                totalSuccess++;
            }
            else{
                emit TransferFailed(recipients[i], values[i]);
                if (revertOnfail){
                    require(success, "One of the transfers failed");
                }
                     
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

    modifier onlyOwner() {
        require(msg.sender == owner, "Can't call this function");
        _;
    }
}
