from flask import Flask, jsonify, request
from injector import Injector

from src.domain.parameters.movie_parameters import MovieParameters
from src.services.movie_services import MovieServices
from src.deps.dependencies import AppModule
from src.domain.parameters.ticket_parameters import TicketParameters

injector = Injector(AppModule())
movie_service = injector.get(MovieServices)

app = Flask(__name__)

@app.route('/tix/movie/<string:id>', methods=['GET'])
def get_movie_by_id(id : str):
    try:
        result = movie_service.get_movies_by_id(id)

        if result is None:
              return jsonify({
                 "error_message" :  "Movie Not found"
             }), 404    

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'message': 'An error occurred: {}'.format(str(e))}), 500      



@app.route('/tix/movie', methods=['POST'])
def add_movie():
    try:
        json_data = request.get_json() 
        params = MovieParameters(
             image=json_data['image'],
             movie_name =json_data['movie_name'],
             genre =json_data['genre'],
             price =json_data['price'],
             tickets=json_data['tickets'],
             max_tickets=json_data['max_tickets'],
             cinema_area=json_data['cinema_area'],
             remarks=json_data['remarks'],
             time=json_data['time'],
             location=json_data['location'],
             lftrb_ratings=json_data['lftrb_ratings']
        )
        
        movie_id = movie_service.create_movie(params)

        if movie_id == '':
              return jsonify({
                 "error_message" :  "Failed to insert movie"
             }), 500    


        return jsonify({
             "movie_id" : movie_id
        }), 200
    
    except Exception as e:
          return jsonify({'message': 'An error occurred: {}'.format(str(e))}), 500    


@app.route('/tix/movie/nft/<int:token_id>', methods=['GET'])
def get_token(id : int):
     try:

          return jsonify({
             "token_url" : movie_service.get_token_uri(id)
            }), 200

     except Exception as e:
        return jsonify({'message': 'An error occurred: {}'.format(str(e))}), 500    


@app.route('/tix/movie/<string:movie_id>', methods=['POST'])
def buy_ticket(movie_id : str):
     try:
          json_data = request.get_json() 

          meta_data_url = movie_service.mint_tickets(
               contact_address= json_data['contact_address'],
               secret_key=json_data['secret_key'],
               seat=json_data['seat'], 
               movie_id=movie_id )     
          
          if meta_data_url is None:
              return jsonify({'message': 'Failed to buy ticket'}), 500    

          return jsonify({
             "movie_id" : meta_data_url.movie_id,
             "token_url" : meta_data_url.token_uri
            }), 200

     except Exception as e:
        return jsonify({'message': 'An error occurred: {}'.format(str(e))}), 500    
         




if __name__ == '__main__':
    app.run(port=8999,debug=True,host='0.0.0.0')


