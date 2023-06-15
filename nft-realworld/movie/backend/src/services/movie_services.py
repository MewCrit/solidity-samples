import uuid
import os
import requests


from typing import Dict
from injector import inject
from src.domain.dto.movie_dto import MovieDTO
from src.domain.entity.movie import Movie
from src.domain.parameters.movie_parameters import MovieParameters
from src.repo.movie_repo import MovieRepository
from dotenv import load_dotenv
from datetime import date


load_dotenv()

class MovieServices:

    @inject
    def __init__(self, movie_repo: MovieRepository) :
        self.movie_repo =  movie_repo
    
    def get_movies_by_id(self, id : str):
        return self.movie_repo.get_movies_by_id(id)
    
    
    def create_movie(self, dto: MovieParameters):

        guid = uuid.uuid4()
        id = str(guid)

        return self.movie_repo.add_movies(
            id= id,
            image=dto.image,
            movie_name= dto.movie_name,
            max_tickets= dto.max_tickets,
            cinema_area= dto.cinema_area,
            remarks=dto.remarks,
            genre=dto.genre,
            lftrb_ratings=dto.lftrb_ratings,
            location=dto.location,
            price= dto.price,
            tickets=dto.tickets,
            time=dto.time
        )
    

    def mint_tickets(self, contact_address : str,  seat : str, movie_id : str) -> MovieDTO:
        try:
            
            get_movie = self.movie_repo.get_movies_by_id(movie_id)
            movie_name = f"{get_movie.movie_name}-{get_movie.id}"
            ticket_meta_data = transform_metadata(movie_name=movie_name, seat=seat, get_movie=get_movie)
            urls = upload_to_pinata(ticket_meta_data)
            id = self.movie_repo.mint_nft_tickets(contact_address,  seat, movie_id, urls, get_movie.price)

            movie_dto = MovieDTO(movie_id= id, token_uri=urls)

            return movie_dto
        except Exception as e:
            print(e)
            return None
        
    def generate_token_uri(self, movie_id  : str, seat : str) -> str:
          try:
            get_movie = self.movie_repo.get_movies_by_id(movie_id)
            movie_name = f"{get_movie.movie_name}-{get_movie.id}"
            ticket_meta_data = transform_metadata(movie_name=movie_name, seat=seat, get_movie=get_movie)

            urls = upload_to_pinata(ticket_meta_data)
            return urls
          except Exception as e:
            print(e)
            return None


    def get_token_uri(self, token_id : int) -> str:
        return self.movie_repo.get_token_uri(token_id=token_id)


    def get_all_movies(self):
        return self.movie_repo.get_all_movies()




def upload_to_pinata(json_data : Dict) -> str:

    pinata_url = os.environ.get('PINATA_URL')
    pinata_api_key = os.environ.get('PINATA_KEY')
    pinata_secret_ket = os.environ.get('PINATA_SECRET')

    headers = {
        'pinata_api_key': pinata_api_key,
        'pinata_secret_api_key': pinata_secret_ket,
        'Content-Type': 'application/json'
    }
    response = requests.post(f'{pinata_url}/pinning/pinJSONToIPFS', 
                                 json=json_data, 
                                 headers=headers)
        
    print(response.json())

    response_json = response.json()
    cid = response_json['IpfsHash']
    ipfs_url = f'https://gateway.pinata.cloud/ipfs/{cid}'
    
    return ipfs_url



def transform_metadata(movie_name : str, seat : str, get_movie: Movie):
    return {
             "name" : movie_name,
             "image" : get_movie.image,
             "description" : get_movie.remarks,
             "attributes" : [
                 {
                     "trait_type" : "Unique ID",
                     "value": get_movie.id
                 },
                 {
                     "trait_type": "LFTRB Rating",
                     "value": get_movie.lftrb_ratings
                 },
                 {
                     "trait_type": "Cinema Area",
                     "value": get_movie.cinema_area
                 },  
                 {
                     "trait_type": "Schedule",
                     "value": get_movie.time
                 },
                 {
                     "trait_type": "Seat",
                     "value": seat
                 },
                 {
                     "trait_type": "Location",
                     "value": get_movie.location
                 }
             ]
        }





        # bucket_name = os.environ.get('S3_BUCKETNAME')

        # folder = 'metadata'
        
        # file_key = f'{folder}/{file_name}'

        # s3 = boto3.client('s3')
        # s3.put_object(Bucket=bucket_name, Key=file_key, Body=convert_to_json)

        # get_url = s3.generate_presigned_url(
        #             ClientMethod='get_object',
        #             Params={
        #                  'Bucket': bucket_name,
        #                  'Key': file_key
        #             }
        #     )