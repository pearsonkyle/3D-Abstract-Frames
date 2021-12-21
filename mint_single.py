import os
from eth_account import Account
from contract import SmartContract

if __name__ == "__main__":
    # Trys to mint a NFT from this contract:
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

        mint_price = evm.call("getMintPrice") # wei

        # mint NFT if conditions are met
        if evm.balance_wei > mint_price and supply > 0:

            # default "to" value is contract address
            tx_hash = evm.transfer(value=mint_price) # units are wei

            print(SmartContract.explorer(network).format(tx_hash))
            print("waiting for receipt...")

            tx_receipt = evm.w3.eth.wait_for_transaction_receipt(tx_hash)
            print(tx_receipt)