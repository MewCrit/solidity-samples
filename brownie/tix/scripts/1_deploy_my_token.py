from brownie import accounts, config, MyToken

initial_supply = 100000000000000000000000000000000000000000000000

def main():
    account = accounts[0]
    erc20 = MyToken.deploy(initial_supply, {"from": account})
