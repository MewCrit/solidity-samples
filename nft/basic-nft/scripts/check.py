import os
from brownie import Pokemon

def main():
    if len(Pokemon) > 0:
        pokemon = Pokemon[len(Pokemon) - 1] 
    else:
        print("No deployed Pokemon contracts found.")
        return

    tokenId = 1

    owner = pokemon.ownerOf(tokenId)
    print(f"Owner of token ID {tokenId} is {owner}")

    uri = pokemon.tokenURI(tokenId)
    print(f"URI of token ID {tokenId} is {uri}")

    balance = pokemon.balanceOf(owner)
    print(f"Balance of the owner is {balance}")
