

import json
import os
from web3 import Web3

class Web3Utility:
    def __init__(self, ps=None, token_to_buy=None, private_key=None, abi=None, network="BSC"):
        path = os.path.dirname(os.path.realpath(__file__))
        with open(f"{path}/chain_configs.txt", "r") as f:
            chain_configs = json.loads(f.read())
        if network == "BSC":
            rpc = "https://data-seed-prebsc-1-s1.binance.org:8545/"
            rpc_ws = "wss://bsc-ws-node.nariox.org:443"
            self.web3WS = Web3(Web3.WebsocketProvider(rpc_ws))
        else:
            rpc = chain_configs[network]["url"]
        self.chain_id = chain_configs[network]["id"]
        self.gas_limit = 200000
        self.gas_price = 10
        self.web3 = Web3(Web3.HTTPProvider(rpc))
        if self.web3.isConnected():
            print("Initiated Web3 object.")
        else:
            print("RPC failed.")
            return
        self.get_token_to_buy = token_to_buy
        self.private_key = private_key
        self.ps = ps
        if not abi:
            current_path = os.path.dirname(os.path.realpath(__file__))
            with open(f"{current_path}/abi.txt", "r") as f:
                abi = json.loads(f.read())
        
        if token_to_buy:
            self.contract = self.web3.eth.contract(address=self.web3.toChecksumAddress(token_to_buy), abi=abi)

    def get_eth_balance(self, address):
        address = self.web3.toChecksumAddress(address)
        bnb_balance = self.web3.eth.getBalance(address)
        bnb_balance = self.web3.fromWei(bnb_balance, 'ether')
        return bnb_balance

    def get_token_balance(self, address):
        token_balance = self.contract.functions.balanceOf(
            self.web3.toChecksumAddress(address)).call()
        return self.web3.fromWei(token_balance, 'ether')

    def estimateGas(self, txn):
        gas = self.web3.eth.estimateGas({
            "from": txn['from'],
            "to": txn['to'],
            "value": txn['value'],
            "data": txn['data']
        })
        gas = gas + (gas / 10)  # Adding 1/10 from gas to gas!
        return gas

    def is_approve(self, address):
        Approve = self.contract.functions.allowance(
            address, self.web3.toChecksumAddress(self.ps.router_address)).call()
        Aproved_quantity = self.contract.functions.balanceOf(address).call()
        if int(Approve) <= int(Aproved_quantity):
            return False
        else:
            return True

    def approve(self, address):
        address = self.web3.toChecksumAddress(address)
        if not self.is_approve(address):
            txn = self.contract.functions.approve(self.web3.toChecksumAddress(self.ps.router_address), self.web3.toWei(100000, 'ether')).buildTransaction({
                'from': address,
                'gas': self.gas_limit,
                'gasPrice': self.web3.toWei(f'{self.gas_price}', 'gwei'),
                'nonce': self.web3.eth.getTransactionCount(address),
                'value': 0
            })
            txn.update({'gas': int(self.estimateGas(txn))})
            signed_txn = self.web3.eth.account.sign_transaction(
                txn, private_key=self.private_key)
            tx_token = self.web3.eth.send_raw_transaction(
                signed_txn.rawTransaction)
            txn_receipt = self.web3.eth.waitForTransactionReceipt(tx_token)
            # print(txn_receipt)
            if txn_receipt["status"] == 1:
                print("Approved")
                return True
            else:
                return False
        else:
            print("Already approved.")
            return True

    def send_token(self, sender_address, to_address, value):
        sender_address = self.web3.toChecksumAddress(sender_address)
        to_address = self.web3.toChecksumAddress(to_address)
        value = self.web3.toWei(value, 'ether')
        nonce = self.web3.eth.get_transaction_count(sender_address, 'pending')
        build_transaction_data = {
            'from': sender_address,
            'gas': self.gas_limit,
            'gasPrice': self.web3.toWei(f'{self.gas_price}','gwei'),
            'nonce': nonce
        }
        txn = self.contract.functions.transfer(to_address, value).buildTransaction(build_transaction_data)
        signed_txn = self.web3.eth.account.sign_transaction(txn, private_key=self.private_key)
        tx_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return self.web3.toHex(tx_hash)

    def send_bnb(self, sender_address, to_address, value):
        sender_address = self.web3.toChecksumAddress(sender_address)
        to_address = self.web3.toChecksumAddress(to_address)
        value = self.web3.toWei(value, 'ether')
        nonce = self.web3.eth.get_transaction_count(sender_address, 'pending')
        build_transaction_data = {
            'chainId': 97,
            'to': to_address,
            'value': value,
            'gas': self.gas_limit,
            'gasPrice': self.web3.toWei(f'{self.gas_price}','gwei'),
            'nonce': nonce
        }
        txn = build_transaction_data
        signed_txn = self.web3.eth.account.sign_transaction(txn, private_key=self.private_key)
        tx_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return self.web3.toHex(tx_hash)




web3util = Web3Utility(private_key='3890cfdfb7f4bf928961c33e91255292ac77e95454b0b468e224113fed4a400b')
with open('abi.txt','r') as r:
    abi = json.loads(r.read())
nonce = web3util.web3.eth.get_transaction_count('0xE515BA407b97B053F89c4eecb8886F4C6101d4A3')
#sum = sum(value*len)
build_transaction_data = {
            'value': web3util.web3.toWei(1,'ether'),
            'from': '0xE515BA407b97B053F89c4eecb8886F4C6101d4A3',
            'gas': 300000,
            'gasPrice': web3util.web3.toWei(f'{web3util.gas_price}','gwei'),
            'nonce': nonce
        }
contract = web3util.web3.eth.contract(address=web3util.web3.toChecksumAddress('0x1990c7e01302F004594A3E5c54dcfD51176853DD'), abi=abi)
tx_data = contract.functions.scatterEther([web3util.web3.toChecksumAddress('0x66707b95dFCC2C17f37CeeE0037A17078431814A'),web3util.web3.toChecksumAddress('0x66707b95dFCC2C17f37CeeE0037A17078431814A')],[int(web3util.web3.toWei(0.01,'ether')),int(web3util.web3.toWei(0.01,'ether'))],True).buildTransaction(build_transaction_data)
signed_txn = web3util.web3.eth.account.sign_transaction(tx_data, private_key='6719332b9ce8b1b26fa66650c79237948e7b2072f1d2031b1370bd1c2a33ac93')
tx_token = web3util.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
print(web3util.web3.toHex(tx_token))