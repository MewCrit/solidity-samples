import React, { useEffect, useState } from "react";
import Web3 from 'web3';

import { Header } from "../components/Header";
import { Footer } from "../components/Footer";

import './HomePage.css'
import { Box, Button, Card, CardContent, CardMedia, Container, Grid, Stack, Typography, Drawer, Modal, List, ListItem, ListItemText } from "@mui/material";
import { MovieModel } from "../models/MovieModel";
import {generateTokenURI, getMovies} from '../services/apiService'

import ABI from '../abi/Tixer.json'


declare global {
  interface Window {
    ethereum: any;
  }
}

// a ganache contract address
const contractAddress = '0x6931aa877c177ffebdf0416f30e73e5abaeb6eba'


export const HomePage: React.FC = () => {
  const web3 = new Web3(window.ethereum);

  const [selectedMovie, setSelectedMovie] = useState<MovieModel | null>(null);
  const [movies, setMovies] = useState<MovieModel[]>([]);
  const [openModal, setOpenModal] = useState(false);
  const [contract, setContract] = useState<any | null>(null);
  const [account, setAccount] = useState<string | null>(null);
  const [movieID, setMovieID] = useState('');
  const [price, setPrice] = useState('');

  useEffect(() => {

      const getAccount = async () => {
        if (window.ethereum) {
            try {  
                    const contractInstance = new web3.eth.Contract(ABI.abi, contractAddress);
                    setContract(contractInstance);
               
            } catch (error) {
                console.error(error);
            }
        }
    };
    getAccount();

  
    const fetchMovies = async () => {
      const moviesData = await getMovies();
      setMovies(moviesData);
    };
    fetchMovies();

  
  }, []);
  
  const handleOpenModal = () => {
    setOpenModal(true);
  };

  const handleCloseModal = () => {
    setOpenModal(false);
  };

     
  const body = (
    <Box
      sx={{
        position: 'absolute',
        top: '50%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
        width: 400,
        bgcolor: 'background.paper',
        border: '2px solid #000',
        boxShadow: 24,
        p: 4,
      }}
    >
      <Typography id="modal-modal-title" variant="h6" component="h2">
        Seat Selection
      </Typography>
      <Box
        sx={{
          display: 'grid',
          gridTemplateColumns: 'repeat(5, 1fr)',
          gap: 2,
          my: 2,
        }}
      >
        {Array.from({ length: 50 }, (_, i) => (
             <Button 
             variant="outlined" 
             key={i}
             onClick={async () => {
               const seatNumber = i + 1; 
               
                if (!contract) {
                  console.error('Contract not loaded yet');
                  return;
                }

              // TODO : should not generate NFT from API every time user clicks a seat
               const tokenURI = await generateTokenURI(movieID, seatNumber.toString())
               const accounts = await window.ethereum.request({ method: 'eth_requestAccounts' });
                contract.methods.mintTicket(seatNumber.toString(), movieID, tokenURI)
                .send({ from: accounts[0], value: web3.utils.toWei(price, 'ether')})
                .on('receipt', console.log)
                .on('error', (error : any) => {
                  if (error.message.includes("User denied transaction signature")) {
                      alert("User denied transaction");
                  } else {
                      console.error(error);
                  }
                  });
             }}
           >
             Seat {i + 1}
           </Button>
        ))}
      </Box>
      <Typography variant="h6" component="h2" align="center">
        Screen
      </Typography>
      <Box
        sx={{
          height: 20,
          bgcolor: 'text.primary',
          mt: 2,
        }}
      />
    </Box>
  );
  

  return(
    <>
        <Header name={'Tixers Movie'}/>
        <Box
          sx={{
            bgcolor: 'background.paper',
            pt: 8,
            pb: 6,
          }}
        >
          <Container maxWidth="sm">
            <Typography
              component="h1"
              variant="h2"
              align="center"
              color="text.primary"
              gutterBottom
            >
              <img src="https://upload.wikimedia.org/wikipedia/commons/d/d0/Eth-diamond-rainbow.png" height="250" /><br/>
              TIXER MOVIES
            </Typography>
            <Typography variant="h5" align="center" color="text.secondary" paragraph>
              Watch and buy movie tickets with Ethereum.
            </Typography>
         
          </Container>
        </Box>
        <Container sx={{ py: 2 }} maxWidth="md">
        <h2>NOW SHOWING!!</h2>
          <Grid container spacing={4}>
           
            {movies.map((movie) => (
              <Grid item  xs={12} sm={6} md={4}>
                <Card
                  sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}
                  onClick={() => {
                    setSelectedMovie(movie)
                    setMovieID(movie.id)
                    setPrice(movie.price.toString())
                  }}
                >
                  <CardMedia
                    component="div"
                    sx={{
                      pt: '56.25%',
                    }}
                    image={movie.image}
                  />  
                  <CardContent sx={{ flexGrow: 1 }}>
                    <Typography gutterBottom variant="h5" component="h2">
                      {movie.movie_name}
                    </Typography>
                  </CardContent>
                
                </Card>
              </Grid>
            ))}
          </Grid>
        </Container>
        <Drawer anchor="right" open={selectedMovie !== null} onClose={() => setSelectedMovie(null)}>
        {selectedMovie && (
          <Box sx={{ width: 550, p: 3 }}>
            <img src={selectedMovie.image} height="350" width="300" alt={selectedMovie.movie_name} />
            <Typography variant="h5">{selectedMovie.movie_name}</Typography>
            <p>{selectedMovie.remarks}</p>
             
            <Button variant="contained" color="success" size="large" onClick={handleOpenModal}>
              BUY
            </Button>
            <Card sx={{ width: '100%', marginBottom: '1em' }}>
              
                <CardContent>
                <List>
                  <ListItem>
                      <ListItemText primary="Genre" secondary={selectedMovie.genre} />
                  </ListItem>
                  <ListItem>
                      <ListItemText primary="Ratings" secondary={selectedMovie.lftrb_ratings} />
                  </ListItem>
                  <ListItem>
                      <ListItemText primary="Location" secondary={selectedMovie.location} />
                  </ListItem>
                  <ListItem>
                      <ListItemText primary="Time" secondary={selectedMovie.time} />
                  </ListItem>
                  <ListItem>
                      <ListItemText primary="Price" secondary={`${selectedMovie.price} ETH`} />
                  </ListItem>
                  <ListItem>
                      <ListItemText primary="Remaining Tickets" secondary={selectedMovie.tickets} />
                  </ListItem>
              </List>

                </CardContent>
            </Card>
         

            <Modal
              open={openModal}
              onClose={handleCloseModal}
              aria-labelledby="modal-modal-title"
            >
              {body}
            </Modal>
          </Box>
        )}
      </Drawer>
    </>
)

}
