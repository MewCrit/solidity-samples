from dataclasses import dataclass

@dataclass
class Movie:
    id: str
    image : str
    movie_name: str
    genre: str
    price: float
    tickets: int
    max_tickets: int
    cinema_area: int
    remarks: str
    time: str
    location: str
    lftrb_ratings: str
