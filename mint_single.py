import os
from eth_account import Account
from contract import SmartContract

if __name__ == "__main__":
    # Trys to mint and NFT from this collections:
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