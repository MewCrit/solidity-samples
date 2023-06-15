import axios from 'axios';
import { MovieModel } from '../models/MovieModel';

const BASE_URL = 'http://127.0.0.1:8999/tix'

export const getMovies = async (): Promise<MovieModel[]> => {
  try {
    const response = await axios.get(`${BASE_URL}/movie`);
    return response.data.results; 
  } catch (error) {
    console.error('Failed to fetch movies', error);
    return [];
  }
};


export  const generateTokenURI = async (movie_id : string, seat_name: string): Promise<string> => {
    try {
        const response = await axios.post(`${BASE_URL}/movie/token_uri/${movie_id}?seat=${seat_name}`);
        return response.data.results; 
      } catch (error) {
        console.error('Failed to generate token uri', error);
        return "";
      }
}