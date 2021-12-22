import os
import json

from web3 import Web3
from web3.middleware import geth_poa_middleware

network_chainid = {
    'polygon':0x89,
    'mainnet':0x1,
    'mumbai':80001,
    'ropsten':0x3,
    'rinkeby':0x4
}

network_unit = {
    'polygon':'matic',
    'mumbai':'matic',
    'mainnet':'ether',
    'ropsten':'ether',
    'rinkeby':'ether'
}

# rpc endpoints
infura_url = {
    'polygon':f"https://polygon-mainnet.infura.io/v3/{os.environ['WEB3_INFURA_PROJECT_ID']}",
    'mumbai':f"https://polygon-mumbai.infura.io/v3/{os.environ['WEB3_INFURA_PROJECT_ID']}"
}

blockexplorer = {
    'polygon':"https://polygonscan.com/tx/{}",
    'mumbai':'https://mumbai.polygonscan.com/tx/{}'
}

class SmartContract():
    
    def __init__(self, account, contract_address, abi, network):
        if isinstance(abi, str):
            if os.path.exists(abi):
                self.abi = json.load(open(abi,"r"))
            else:
                raise Exception("abi file not found")
        elif isinstance(abi, dict):
            self.abi = abi
        else:
            raise Exception("abi must be a file path or dictionary")

        self.account = account
        self.contract_address = contract_address

        self.w3 = Web3(Web3.HTTPProvider(infura_url[network]))
        self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)

        self.chain_id = network_chainid[network]
        self.contract = self.w3.eth.contract(address=self.w3.toChecksumAddress(contract_address), abi=self.abi)
        self.gasPrice = '20' # gwei
        self.gas = 2000000

    def call(self, function_name, *args):
        return self.contract.functions[function_name](*args).call()

    def transfer(self, **kwargs):
        # build basic transaction
        tx_hash = {
            'to':kwargs.get('to',self.w3.toChecksumAddress(self.contract_address)), 
            'nonce':self.nonce,
            'value': kwargs.get("value",1), # <- UNITS
            'gasPrice': 2000000000,
            'gas': 200000,
            'chainId':kwargs.get('chainId',self.chain_id)
        }
    
        # sign transaction
        signed_txn = self.w3.eth.account.sign_transaction(tx_hash, private_key=self.account.privateKey)

        # send transaction
        tx_sent = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)

        return tx_sent.hex()

    def transact(self, function_name, *args, **kwargs):
        tx_hash = self.contract.functions[function_name](*args).buildTransaction({
            'from':self.account.address, 
            'nonce':kwargs.get('nonce', self.nonce), 
            'gasPrice': self.w3.toHex(self.w3.toWei(kwargs.get('gasPrice',self.gasPrice), 'gwei')),
            'chainId':kwargs.get('chainId',self.chain_id)})

        # sign transaction
        signed_txn = self.w3.eth.account.sign_transaction(tx_hash, private_key=self.account.privateKey)
        # send transaction
        tx_sent = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return tx_sent.hex()

    @property
    def balance(self):
        return self.w3.fromWei(self.w3.eth.get_balance(self.account.address),'ether')

    @property
    def balance_wei(self):
        return self.w3.eth.get_balance(self.account.address)

    @property
    def nonce(self):
        return self.w3.eth.get_transaction_count(self.account.address)

    @staticmethod
    def unit(network):
        return network_unit[network]
    
    @staticmethod
    def explorer(network):
        return blockexplorer[network]

