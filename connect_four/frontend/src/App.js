import React, { Component } from 'react';
import './App.css';
import GameBoard from './GameBoard';

class App extends Component {
  render() {
    return (
      <div className="">
          <header className="center max-width">
              <h2>Connect 4</h2>
          </header>
          <GameBoard />
      </div>
    );
  }
}

export default App;
