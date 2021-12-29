// SPDX-License-Identifier: MIT
// matic main - 0x5FdEA8CB5C974d274957e8bE7318BE1489FC8896
// matic test - 0x48be78204C7D3cC3A6656c69450F2DAcd910fA3e
pragma solidity ^0.8.0;

import "openzeppelin-solidity/contracts/access/Ownable.sol";
import "openzeppelin-solidity/contracts/token/ERC721/ERC721.sol";

contract AbstractFrame3D is 
    ERC721,
    Ownable
{
    // total number minted
    uint private token; 

    // price to mint
    uint256 private mint_price;

    // map token id to NFT metadata
    mapping(uint256 => string) private token2uri;

    // storage for current NFT drop
    string[4444] private uris;
    
    // ending index for current drop
    uint256 private dropSize = 0; 

    // keeps track of how many times a given address minted
    mapping(address => uint256) private address2mints;
    address[4444] private addressInDrop;
    uint256 private dropIdx = 0; // current position in  drop
    
    // number of mints each person can do per drop
    uint256 private max_mint = 5;

    // Wearable Augmented Reality
    constructor() public ERC721("3D Abstract Frames", "3D af") {
        token = 1;
        mint_price = 0; // wei
    }

     /////////////////////////////////////////////////////////////////////////////
     // public methods - anyone
    function getMintPrice()
        public 
        view
        returns (uint256)
    {
        return mint_price; // wei
    }

    // transfer tokens to contract and get a nft
    receive() external payable
    {
        require(msg.value >= mint_price, "NFT: check getMintPrice()");
        require(dropIdx < dropSize, "NFT: no more NFTs in collection");
        require(address2mints[msg.sender] < max_mint, "NFT: user minted max value");

        // if first time minter
        if (address2mints[msg.sender] == 0)
        {
            addressInDrop[dropIdx] = msg.sender;
        }

        _mint(msg.sender, token);           // send ERC721 token
        token2uri[token] = uris[dropIdx];   // save meta data to token
        address2mints[msg.sender]++;        // add minting counter for given address
        dropIdx++;                          // advance to next idx in drop
        token++;                            // keep track of all NFTs minted
    }

    function burn(
        uint256 _tokenId
    )
     external
    {
        address owner = ERC721.ownerOf(_tokenId);
        require(msg.sender == owner, "ERC721: approval to current owner");
        _burn(_tokenId);
    }

    function tokenURI(
        uint256 _tokenId
    ) 
     public view virtual override 
     returns (string memory)
    {
        require(_exists(_tokenId), "ERC721Metadata: URI query for nonexistent token");
        return token2uri[_tokenId];
    }

    // print NFTs left in collection
    function tokenSupply() public view returns(uint256){
        return dropSize-dropIdx;
    }

    function getDropSize()
     public view
     returns (uint256)
    {
        return dropSize;
    }

    /////////////////////////////////////////////////////////////////////////////
    // contract owner methods

    function setMintPrice(uint256 _price)
        public
        onlyOwner
    {
        mint_price = _price;
    }

    function getContractBalance() 
        public 
        view 
        onlyOwner 
        returns(uint) 
    {
        return address(this).balance;
    }

    function withdrawContractBalance() public onlyOwner {
        address payable to = payable(msg.sender);
        to.transfer(getContractBalance());
    }

    function addToURIs(string calldata _uri)
     external
     onlyOwner
    {
        uris[dropSize] = _uri;
        dropSize++;
    }

    function addToURIs(string[] calldata _uris)
     external
     onlyOwner
    {
        for(uint i=0; i<_uris.length; i++)
        {
            uris[dropSize] = _uris[i];
            dropSize++;
        }
    }

    function getDropURI(uint256 idx)
     view public
     onlyOwner
     returns (string memory)
    {
        require(idx < dropSize, "NFT: idx too large");
        return uris[idx];
    }

    // set up for a new drop
    function resetCollection()
     external
     onlyOwner
    {
        // cycle through URIs again
        dropSize = 0;
        dropIdx = 0;

        // everybody can mint again
        for(uint i=0; i<addressInDrop.length; i++)
        {
            address2mints[addressInDrop[i]] = 0;
        }
    }

    function autoMint(address _to, string calldata _uri)
        external
        onlyOwner
    {
        _mint(_to, token);
        token2uri[token] = _uri;
        token++;
    }

    function burnBatch(
        uint256[] calldata _tokenIds
    )
     external
     onlyOwner
    {
        for (uint i=0; i<_tokenIds.length; i++)
        {
            _burn(_tokenIds[i]);
        }
    }

    function updateMetadataOwner(
        uint256 _tokenId,
        string calldata _uri
    )
     external
     onlyOwner
    {
        token2uri[_tokenId] = _uri;
    }
}