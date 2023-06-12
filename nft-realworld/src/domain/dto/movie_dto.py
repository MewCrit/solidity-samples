

class MovieDTO:
    movie_id : str
    token_uri : str

    def __init__(self, movie_id :str, token_uri : str):
        self.movie_id = movie_id
        self.token_uri = token_uri