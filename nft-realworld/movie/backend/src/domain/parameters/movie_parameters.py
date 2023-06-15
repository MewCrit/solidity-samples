

class MovieParameters:
    image : str
    movie_name: str
    genre: str
    price: int
    tickets: int
    max_tickets: int
    cinema_area: int
    remarks: str
    time: str
    location: str
    lftrb_ratings: str

    def __init__(self, image : str,  movie_name : str, genre : str, price : int,  tickets : int, max_tickets :int,  cinema_area : int, remarks:str, time : str, location : str, lftrb_ratings : str):
            self.image = image
            self.movie_name = movie_name   
            self.genre = genre        
            self.price = price        
            self.tickets = tickets      
            self.max_tickets = max_tickets  
            self.cinema_area = cinema_area  
            self.remarks = remarks      
            self.time = time         
            self.location = location     
            self.lftrb_ratings = lftrb_ratings

