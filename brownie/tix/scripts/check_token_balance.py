from brownie import MyToken, accounts

def main():
    account = accounts[0]
    contract_address = '0x3ea9af16de581c88a5b823b7923edc238901d1d3'

    my_token = MyToken.at(contract_address)

    total_supply = my_token.totalSupply()
    print("Total supply is:", total_supply)
    balance = my_token.balanceOf(account)

    print("The balance of account", account, "is:", balance)
