from hashlib import sha3_224
from brownie import chain, network, accounts, config

def get_account():
    if network.show_active() == True:
        return accounts[0]
    else:
        return accounts.add(config['wallets']['from_key'])
    
