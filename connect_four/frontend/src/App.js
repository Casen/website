import React, { Component } from 'react';
import './App.css';
import Game from './Game';

class App extends Component {
  render() {
    return (
      <div className="">
        <header className="center max-width">
            <h2>Play Connect 4</h2>
        </header>
        <p className="center">The rules are simple: be the first to connect four moves either horizontally or vertically.</p>
        <Game/>
      </div>
    );
  }
}

export default App;
