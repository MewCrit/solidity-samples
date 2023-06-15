import React from 'react';
import { BrowserRouter as Router, Switch, Route, HashRouter } from "react-router-dom";
import './App.css';
import { HomePage } from './pages/HomePage';

function App() {
  return (
    <Router>
      <Switch>
           <Route exact path="/">
              <HomePage />
            </Route>
      </Switch>


    </Router>
  );
}

export default App;
