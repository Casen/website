import React, { Component } from 'react';
import './App.css';
import Game from './Game';

class App extends Component {
  render() {
    return (
      <div className="">
          <header className="center max-width">
              <h2>Connect 4</h2>
          </header>
          <Game />
      </div>
    );
  }
}

export default App;
