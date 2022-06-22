// SPDX-License-Identifier: MIT

pragma solidity ^0.8.4;

import "./ERC721A.sol";
// import "https://github.com/chiru-labs/ERC721A-Upgradeable/blob/main/contracts/ERC721AUpgradeable.sol";
// import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol";
import "./Ownable.sol";
import "./Counters.sol";

interface ERC20 {
  function balanceOf(address owner) external view returns (uint);
  function allowance(address owner, address spender) external view returns (uint);
  function approve(address owner, address spender, uint amount) external returns (bool);
  function transfer(address to, uint value) external returns (bool);
  function transferFrom(address from, address to, uint value) external returns (bool); 
}

contract NVCNFT is ERC721A, Ownable {
    using Counters for Counters.Counter;
    Counters.Counter private _tokenIdCounter;
    uint256 public constant PRICE = 0.01 ether;
    uint256 public constant COLLECTION_SIZE = 10000;
    address public constant BUSD_CONTRACT = 0x78867BbEeF44f2326bF8DDd1941a4439382EF2A7;
    
    constructor() ERC721A("Next Venture Capital", "NVC") {}

    function _baseURI() internal pure override returns (string memory) {
        return "ipfs://QmbksLtdi1yDJdHcPgVBc5cLyGGs5j4rMq4a4WXFFZu2XG/";
    }

    function safeMint(uint _quantity) public payable {
        require(_quantity > 0, "Quantity must be greater than 0.");
        uint256 currentTokenId = _tokenIdCounter.current();
        require(currentTokenId + _quantity <= COLLECTION_SIZE, "Cannot mint over supply cap");
        //require(mintingOpen == true, "Minting is not open right now!");
        //require(canMintAmount(_to, 1), "Wallet address is over the maximum allowed mints");
        require(transferToken(msg.sender, BUSD_CONTRACT, PRICE * _quantity), "Contract hasn't received the mint fee.");      
        _tokenIdCounter.increment();
        _safeMint(msg.sender, _quantity);
    }
    
    function transferToken(address _owner, address _token, uint _amount) internal returns (bool){
        return ERC20(_token).transferFrom(_owner, address(this), _amount);
    }
    
    function burn(uint256 _tokenId) public {
        require(ownerOf(_tokenId)==msg.sender,"Not the owner.");
        _burn(_tokenId, true);
        emit NftBurned(msg.sender, _tokenId, block.timestamp);
    }

    event NftBurned(address owner, uint256 tokenId, uint256 timestamp);

    function burnBatch(uint256[] memory _tokenIds) public {
        uint256 i = 0;
        for (i; i < _tokenIds.length;i++) {
            require(ownerOf(_tokenIds[i])==msg.sender,"Not the owner.");
            _burn(_tokenIds[i], true);
            emit NftBurned(msg.sender, _tokenIds[i], block.timestamp);
        }
    }
}
