// SPDX-License-Identifier: MIT

pragma solidity ^0.8.4;

import "./extensions/ERC721AQueryable.sol";
import "./utils/Counters.sol";

// import "https://github.com/chiru-labs/ERC721A-Upgradeable/blob/main/contracts/ERC721AUpgradeable.sol";
// import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol";
// import "@openzeppelin/contracts/utils/ERC721/extensions/ERC721Enumerable.sol";

interface IERC20 {
    function transferFrom(
        address from,
        address to,
        uint256 value
    ) external returns (bool);
}

contract NextVisionCapital is ERC721AQueryable {
    event NftBurned(address owner, uint256 tokenId, uint256 timestamp);

    using Counters for Counters.Counter;

    Counters.Counter private _tokenIdCounter;

    uint256 public constant PRICE = 1 ether; //1 BUSD

    uint256 public constant COLLECTION_SIZE = 10000;

    IERC20 public immutable _erc20;

    address public constant ADDRESS_RECEIVER =
        0xE515BA407b97B053F89c4eecb8886F4C6101d4A3;

    constructor(IERC20 erc20_) ERC721A("Next Vision Capital", "NVC") {
        _erc20 = erc20_;
    }

    function baseURI() public pure returns (string memory) {
        return "ipfs://QmbksLtdi1yDJdHcPgVBc5cLyGGs5j4rMq4a4WXFFZu2XG/";
    }

    function safeMint(uint256 _quantity) external payable {
        require(_quantity > 0, "Quantity must be greater than 0.");

        require(
            totalSupply() + _quantity <= COLLECTION_SIZE,
            "Cannot mint over supply cap"
        );

        require(
            transferERC20(msg.sender, PRICE * _quantity),
            "Fail to transfer token."
        );

        _safeMint(msg.sender, _quantity);
    }

    function transferERC20(address _owner, uint256 _amount)
        internal
        returns (bool)
    {
        return _erc20.transferFrom(_owner, ADDRESS_RECEIVER, _amount);
    }

    function burn(uint256 _tokenId) external {
        require(ownerOf(_tokenId) == msg.sender, "Not the owner.");

        _burn(_tokenId);

        emit NftBurned(msg.sender, _tokenId, block.timestamp);
    }

    function burnBatch(uint256[] memory _tokenIds) external {
        uint256 i = 0;

        for (i; i < _tokenIds.length; i++) {
            require(ownerOf(_tokenIds[i]) == msg.sender, "Not the owner.");

            _burn(_tokenIds[i]);

            emit NftBurned(msg.sender, _tokenIds[i], block.timestamp);
        }
    }

    function totalMinted() public view returns (uint256) {
        return _totalMinted();
    }

    function totalBurned() public view returns (uint256) {
        return _totalBurned();
    }
}
