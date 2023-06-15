

class MovieDTO:
    movie_id : str
    token_uri : str

    def __init__(self, movie_id :str, token_uri : str):
        self.movie_id = movie_id
        self.token_uri = token_uri

    def to_dict(self):
        return {
            'movie_id': self.movie_id,
            'token_uri': self.token_uri
        }