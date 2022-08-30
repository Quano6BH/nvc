// SPDX-License-Identifier: MIT

pragma solidity ^0.8.4;

import "./extensions/ERC721AQueryable.sol";
import "./access/Ownable.sol";

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

contract NextVisionCapital is ERC721AQueryable, Ownable {
    event NftBurned(address owner, uint256 tokenId, uint256 timestamp);

    uint256 public constant COLLECTION_SIZE = 1000;

    string public uri = "ipfs://QmNuJqQLLa2iqZNEXpdHBy9bWTS1KzLdm1rxTFDDi54YQu";
    constructor() ERC721A("NextVisionCapital Collection", "NVC") {
    }

//uri
    function _baseURI() internal view override returns (string memory) {
        return uri;
    }

    function changeBaseURI(string memory newBaseURI) external onlyOwner{
        uri = newBaseURI;
    }

     function tokenURI(uint256 tokenId)
        public
        view
        override
        returns (string memory)
    {
        if (!_exists(tokenId)) revert URIQueryForNonexistentToken();

        string memory baseURI = _baseURI();
        return
            bytes(baseURI).length != 0
                ? string(abi.encodePacked(baseURI, ""))
                : "";
    }

    function safeMintTo(address toAddress ,uint256 _quantity) external onlyOwner{
        require(_quantity > 0, "Quantity must be greater than 0.");

        require(
            totalSupply() + _quantity <= COLLECTION_SIZE,
            "Cannot mint over supply cap"
        );

        _safeMint(toAddress, _quantity);
    }


    function burn(uint256 _tokenId) external onlyOwner {
        require(ownerOf(_tokenId) == msg.sender, "Not the owner.");

        _burn(_tokenId);

        emit NftBurned(msg.sender, _tokenId, block.timestamp);
    }

    function burnBatch(uint256[] memory _tokenIds) external onlyOwner {
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
