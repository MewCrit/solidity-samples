import json
import os

from venv import logger
from web3 import Web3
from dotenv import load_dotenv
from src.domain.dto.movie_dto import MovieDTO
from src.domain.entity.movie import Movie


load_dotenv()

class MovieRepositoryPlaceholder:
    
    def add_movies(self, id : str, image : str, movie_name : str, genre : str, price : int, tickets : int, max_tickets : int, cinema_area : int, remarks : str,  time : str, location : str, lftrb_ratings : str) -> str:
        pass

    def get_movies_by_id(self, id : str) -> Movie:
        pass

    def get_seats_by_id(self, id : str):
        pass

    def mint_nft_tickets(self, contract_address : str, seat : str, movie_id : str, token_uri : str, price :int):
        pass

    def get_token_uri(self, token_id : int) -> str:
        pass


class MovieRepository(MovieRepositoryPlaceholder):

    def add_movies(self, id : str, image : str, movie_name : str, genre : str, price : int, tickets : int, max_tickets : int, cinema_area : int, remarks : str,  time : str, location : str, lftrb_ratings : str)  -> str:
        try:

            web3 = get_web3_config()
            price_in_wei = web3.toWei(price, 'ether')

            contract_address = get_tixer_contract_address()
            secret_key_address = get_contract_secret()
            owner_address = get_contract()

            # Retrieved the smart contracts abi
            with open('../tixer/src/abi/Tixer.json') as f:
                contract_json = json.load(f)  
                contract_abi = contract_json['abi'] 
            
            # Get the nonce value from the address will execute the transaction
            nonce = web3.eth.getTransactionCount(Web3.toChecksumAddress(owner_address))

            # Get the contract address and set the smart contracts abi to identify the "addMovie" function in Solidity.
            movie_contract = web3.eth.contract(address=Web3.toChecksumAddress(contract_address), abi=contract_abi)

            # execute function from solidity
            txn_dict = movie_contract.functions.addMovies(
                                            id, 
                                            image,
                                            movie_name,
                                            genre,
                                            price_in_wei, 
                                            tickets,
                                            max_tickets, 
                                            cinema_area,
                                            remarks, 
                                            time, 
                                            location, 
                                            lftrb_ratings).buildTransaction({
                                                'chainId': 1337,  
                                                'gas': 700000,
                                                'gasPrice': web3.toWei('20', 'gwei'),
                                                'nonce': nonce
                                            })
            
            # This signed transaction can then be sent to the Ethereum network
            # The "secret_key_address" is from the address that will execute this transaction
            signed_txn = web3.eth.account.signTransaction(txn_dict, secret_key_address)
            tx_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
            
            # Check results of the transaction via reciept
            tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)

            logger.info(f"System info: tx reciept: {tx_receipt['logs']}")
            print(tx_receipt['logs'])

            return id
        
        except Exception as e:
             logger.error(f'Error occurred: {e}') 
             return ''
       
    def get_movies_by_id(self, id : str) -> Movie:
        try:
            web3 = get_web3_config()
            contract_address = get_tixer_contract_address()

            with open('../tixer/src/abi/Tixer.json') as f:
                contract_json = json.load(f)  
                contract_abi = contract_json['abi'] 
                        
            movie_contract = web3.eth.contract(address=Web3.toChecksumAddress(contract_address), abi=contract_abi)
            movie = movie_contract.functions.getMovies(id).call()

            print(movie)

            to_ether = web3.fromWei(movie[4], "ether")

            movie = Movie(
                id= movie[0],
                image=movie[1],
                movie_name=movie[2],
                genre=movie[3],
                price=to_ether,
                tickets=movie[5],
                max_tickets=movie[6],
                cinema_area=movie[7],
                remarks=movie[8],
                time=movie[9],
                location=movie[10],
                lftrb_ratings=movie[11]
            )
            
            return movie
        
        except Exception as e:
            logger.error(f'Error occurred: {e}') 
            return None
        

    def get_seats_by_id(self, id : str):
        try:
            web3 = get_web3_config()
            contract_address = get_tixer_contract_address()

            with open('../tixer/src/abi/Tixer.json') as f:
                contract_json = json.load(f)  
                contract_abi = contract_json['abi'] 
                        
            movie_contract = web3.eth.contract(address=Web3.toChecksumAddress(contract_address), abi=contract_abi)
            seats = movie_contract.functions.getSeats(id).call()

            return seats
        
        except Exception as e:
            logger.error(f'Error occurred: {e}') 
            return None


    def mint_nft_tickets(self, contract_address : str, secret_key : str, seat : str, movie_id : str, token_uri : str, price :int):
        try:
            web3 = get_web3_config()
            tixer_contract_address = get_tixer_contract_address() 

            # always convert decimals to wei because solidity doesn't have decimal floating points
            wei = web3.toWei(price, 'ether')

            with open('../tixer/src/abi/Tixer.json') as f:
                contract_json = json.load(f)  
                contract_abi = contract_json['abi'] 
            
            nonce = web3.eth.getTransactionCount(Web3.toChecksumAddress(contract_address))
            movie_contract = web3.eth.contract(address=Web3.toChecksumAddress(tixer_contract_address), abi=contract_abi)

            #
            txn_dict = movie_contract.functions.mintTicket(
                seat,
                movie_id,
                token_uri
            ).buildTransaction({
                  'chainId': 1337,  
                  'gas': 700000,
                  'gasPrice': web3.toWei('20', 'gwei'),
                  'nonce': nonce,
                  'value':wei
            })
        
            signed_txn = web3.eth.account.signTransaction(txn_dict, secret_key)
            tx_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
            tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)

            logger.info(f"System info: tx reciept: {tx_receipt['logs']}")
            print(tx_receipt['logs'])

            return id
        
        except Exception as e:
             logger.error(f'Error occurred: {e}') 
             return ''
        

    def get_token_uri(self, token_id : int) -> str:
        try:
            web3 = get_web3_config()
            tixer_contract_address = get_tixer_contract_address() 
            
            with open('../tixer/src/abi/Tixer.json') as f:
                contract_json = json.load(f)  
                contract_abi = contract_json['abi'] 
            
            movie_contract = web3.eth.contract(address=Web3.toChecksumAddress(tixer_contract_address), abi=contract_abi)
            nft_url = movie_contract.functions.tokenURI(token_id).call()

            return nft_url

        except Exception as e:
            logger.error(f'Error occured: {e}')
            return ''

  

def get_web3_config() -> Web3:
    rpc_url = os.environ.get("RPC_URL")
    web3 = Web3(Web3.HTTPProvider(rpc_url)) 
    return web3

def get_contract() -> str:
    return os.environ.get("CONTRACT_ADDRESS")

def get_tixer_contract_address() -> str:
    return os.environ.get('TIXER_CONTRACT_ADDRESS')

def get_contract_secret() -> str:
    return os.environ.get('CONTRACT_ADDRESS_PRIVATE_KEY')