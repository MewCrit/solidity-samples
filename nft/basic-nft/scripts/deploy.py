from brownie import Pokemon, accounts

def main():
    #  ganache account  
    acct = '0x7f962a7590425f862AaE94823B34b7F02034974b'
    print(acct) 
    pokemon = Pokemon.deploy({"from": acct})
    tokenId = 1
    tokenURI = "https://link.storjshare.io/jvv2q354vd3fy4zg2ovvjgzwcrka/pkmn-nfts%2Fmetadata%2Fcharmander.json"
    pokemon.mint(acct, tokenId, tokenURI, {"from": acct})
