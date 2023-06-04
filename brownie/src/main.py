import json
from web3 import Web3

web3 = Web3(Web3.HTTPProvider('http://localhost:8545')) 

contract_address = '0x3ea9af16de581c88a5b823b7923edc238901d1d3' 

with open('MyToken.json') as f:
    contract_json = json.load(f)  
    contract_abi = contract_json['abi'] 

contract = web3.eth.contract(address=Web3.toChecksumAddress(contract_address), abi=contract_abi)


total_supply = contract.functions.totalSupply().call()
print(f'Total supply: {total_supply}')

