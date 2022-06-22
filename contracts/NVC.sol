// SPDX-License-Identifier: MIT

pragma solidity ^0.8.4;

import "https://github.com/chiru-labs/ERC721A/blob/main/contracts/ERC721A.sol";
// import "https://github.com/chiru-labs/ERC721A-Upgradeable/blob/main/contracts/ERC721AUpgradeable.sol";
// import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

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

    constructor() ERC721A("Next Venture Capital", "NVC") {}

    function _baseURI() internal pure override returns (string memory) {
        return "ipfs://QmbksLtdi1yDJdHcPgVBc5cLyGGs5j4rMq4a4WXFFZu2XG/";
    }

/////////////// GENERIC MINT FUNCTIONS
    /*
    * @dev Mints a single token to an address.
    * fee may or may not be required*
    * @param _to address of the future owner of the token
    */
    function safeMint(uint _quantity) public payable {
        
        uint256 currentTokenId = _tokenIdCounter.current();
        require(currentTokenId + _quantity <= COLLECTION_SIZE, "Cannot mint over supply cap");

        //require(mintingOpen == true, "Minting is not open right now!");

        //require(canMintAmount(_to, 1), "Wallet address is over the maximum allowed mints");

        require(msg.value >= PRICE, "Value below required mint fee");
        
        
        _tokenIdCounter.increment();
        _safeMint(msg.sender, _quantity);
    }
    function transferToken(address _owner, address _token, uint _amount) public {
        ERC20(_token).transferFrom(_owner, address(this), _amount);
    }
    //function safeMint(address to) public onlyOwner {
    //    uint256 tokenId = _tokenIdCounter.current();
    //    _tokenIdCounter.increment();
    //   _safeMint(to, tokenId);
    //}

    // The following functions are overrides required by Solidity.

    // function _beforeTokenTransfer(address from, address to, uint256 tokenId)
    //     internal
    //     override(ERC721A, ERC721Enumerable)
    // {
    //     super._beforeTokenTransfer(from, to, tokenId);
    // }

//     function supportsInterface(bytes4 interfaceId)
//         public
//         view
//         override(ERC721, ERC721Enumerable)
//         returns (bool)
//     {
//         return super.supportsInterface(interfaceId);
//     }
}
