from injector import  Injector, inject, Module, provider
from src.repo.movie_repo import MovieRepository
from src.services.movie_services import MovieServices

class AppModule(Module):

  @provider
  def provide_movie_repository(self) -> MovieRepository:
     return MovieRepository()
  
  @provider
  def provide_movie_service(self, movie_repository: MovieRepository) -> MovieServices:
     return MovieServices(movie_repository)
