from brownie import Tixer, accounts

def main():
    account = accounts[0]
    print(f'Deployed to {account}')
    Tixer.deploy("TixerToken", "TXR", {"from": account})