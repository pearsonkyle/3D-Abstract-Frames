import os
import glob
import requests

from eth_account import Account

from contract import SmartContract

if __name__ == "__main__":

    network = 'polygon'

    evm = SmartContract(
        account = Account.privateKeyToAccount(os.environ['PRIVATE_KEY']),
        contract_address="0x5FdEA8CB5C974d274957e8bE7318BE1489FC8896",
        abi = "af3d.json", network = "polygon"
    )
    
    if evm.w3.isConnected():
        print(" balance:", evm.balance, SmartContract.unit(network))

    print(f'Drop size: {evm.call("getDropSize")}')
    print(f'Token Supply: {evm.call("tokenSupply")}')
    try:
        print(f'Token URI: {evm.call("tokenURI",1)}')
    except:
        pass

    # models on disk
    models = glob.glob("/Users/kpearson/Programs/misc/SmartContract/3d_af/models/second_mint/*.glb")
            
    nonce = evm.nonce

    # folder of uploaded data
    base_url = "https://gateway.pinata.cloud/ipfs/QmTPj3rmjruBJpnE3ohEPu4jPB7ZVoRAoow6HKkehQLuQT/" 

    for m, model in enumerate(models):

        # check for full set of data
        if not os.path.exists(model.replace(".glb", "_render.png")):
            continue

        meta_link = os.path.join(base_url,os.path.basename(model.replace(".glb", ".json")))

        # make sure link does not 404
        r = requests.get(meta_link)
        assert(r.status_code == 200)
    
        # NONCE!!!
        #tx_hash = evm.transact("updateMetadataOwner", m+1, meta_link, nonce=nonce) 
        tx_hash = evm.transact("autoMint", evm.account.address, meta_link, nonce=nonce)
        #tx_hash = evm.transact("addToURIs", meta_link, nonce=nonce)

        nonce+=1

        print(f"Tx sent: {SmartContract.explorer(network).format(tx_hash)}")