import React, { useState } from 'react'
import {AppBar, Button, Toolbar, Typography } from '@mui/material';
import Web3 from 'web3';

declare global {
    interface Window {
      ethereum: any;
    }
  }
  
  
interface PropInterface {
    name : string;
}

export const Header : React.FC<PropInterface> = ({name}) => {
    const [account, setAccount] = useState('');
    
    const connectWallet = async () => {
        if (window.ethereum) {
          try {
            const accounts = await window.ethereum.request({ method: 'eth_requestAccounts' });
            setAccount(accounts[0]);
          } catch (error) {
            console.error(error);
          }
        } else {
          alert('Please install MetaMask!');
        }
      };

    return(
        <AppBar position="fixed">
        <Toolbar>
          <Typography variant="h6" sx={{ flexGrow: 1 }}>
            {name}
          </Typography>
          <Button variant="contained" color="secondary" onClick={connectWallet}>
            {account ? `Connected: ${account.substring(0,6)}...${account.substring(account.length-4)}` : 'Connect'}
          </Button>
        </Toolbar>
      </AppBar>
    )
}