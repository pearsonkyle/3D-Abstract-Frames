# 3D-Abstract-Frames

![](images/banner_9.png)

Smart Contract and python scripts for minting non-fungible tokens (ERC 721) using Polygon



## How to mint

```python
from contract import SmartContract

network = 'mumbai'

evm = SmartContract(
    account = Account.privateKeyToAccount(os.environ['PRIVATE_KEY']),
    contract_address="0x48be78204C7D3cC3A6656c69450F2DAcd910fA3e",
    abi = "af3d.json", network = network
)
    
if evm.w3.isConnected():
    print(" balance:", evm.getAccountBalance(),network_unit[network])

    print(f'Drop size: {evm.call("getDropSize")}')
    print(f'Token Supply: {evm.call("tokenSupply")}')
    try:
        print(f'Token URI: {evm.call("tokenURI",1)}')
    except:
        pass

```