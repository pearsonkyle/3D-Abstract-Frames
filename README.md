# 3D-Abstract-Frames

Abstract digital sculptures in a frame. Each frame is double-sided with a 3D mesh on one side and a flat version of the image on the other.

## [View the NFT collection](https://opensea.io/collection/3d-af)

![](images/banner_long_1.png)

Each NFT comes with a metaverse compatible 3D model

![](images/sequence_smal2.gif)

View in the model in augmented reality using the [Galeri](https://www.galeri.co/) app on iOS.

## How to mint from the [Abstract Frame]() collection


### Requirements
- Python 3
- Crypto Wallet

### Dependencies
- [requirements.txt]()


The smart contract for `3D af` is programmed to mint NFTs upon receiving a payment that is greater than the `mint_price`. This can be seen in the `receive()` method in [`af3d.sol`](). Therefore, just transfer funds to the smart contract address and it will mint you an NFT in return. This interface is similar to a gum ball machine, where the contract is loaded with NFTs ahead of time corresponding to a collection and over time people can send people to the contract and the contract returns an NFT. The simple transfer interface is minimal by design and allows easy access to the minting capabilities accross multiple programming languages. For example, one can mint using the interface on polygon explorer like such:



If you're interested in a more programmatic interface for minting check out this code:

```python
from contract import SmartContract

network = 'mumbai'

evm = SmartContract(
    account = Account.privateKeyToAccount(os.environ['PRIVATE_KEY']),
    contract_address="0x48be78204C7D3cC3A6656c69450F2DAcd910fA3e",
    abi = "af3d.json", network = network
)

if evm.w3.isConnected():

    print("Balance:", evm.balance, SmartContract.unit[network])

    print('Total Collection Size:',evm.call("getDropSize"))
    
    supply = evm.call("tokenSupply")
    print('Token Supply:',supply)

    mint_price = evm.call("mint_price") # wei

    if evm.balance_wei > mint_price and supply > 0:

        # mint NFT
        tx_hash = evm.transact("transfer", value=mint_price)

        tx_receipt = evm.w3.eth.wait_for_transaction_receipt(tx_hash)

        print(SmartContract.explorer(network).format(tx_receipt.hex()))
```


For your own sanity, please verify the source code on polyscan with the function below to ensure the safety of your tokens during the minting process. The smart contract processes incoming tokens as such

```js
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
```

The minting function we use inherits from the ERC 721 implementation: https://docs.openzeppelin.com/contracts/2.x/api/token/erc721#ERC721


## Helpful links for smart contract development
- https://solidity-by-example.org/ 
- https://remix.ethereum.org/


## Additional capability

Only the owner of the smart contract can mint this way

```python
tx_hash = evm.contract.functions.autoMint(evm.account.address, meta_link).buildTransaction({
    'from': evm.account.address,
    #'value': w3.toWei(0.001, 'ether'),
    #'chainId': 0x89, # poly main
    'chainId': 0x13881, # mumbai
    #'chainId': 3, # ropsten
    'gasPrice': evm.w3.toHex(evm.w3.toWei('25', 'gwei')), 
    'nonce': nonce
})

nonce+=1

# sign transaction and send
signed_txn = evm.w3.eth.account.sign_transaction(tx_hash, private_key=evm.account.privateKey)

tx_sent = evm.w3.eth.send_raw_transaction(signed_txn.rawTransaction)

print(f"Tx sent: {SmartContract.explorer(network).format(tx_sent.hex())}")
```