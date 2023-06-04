from  web3 import Web3

web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

print()
print(f'Is it connected: {web3.isConnected()}')

print()
print(f'Accounts available {len(web3.eth.accounts)}')

print()

for account in web3.eth.accounts:
    balance = web3.eth.getBalance(account)
    balance_ether = web3.fromWei(balance, 'ether')
    print(f'Address : {account} \t Balance: {balance_ether}')
