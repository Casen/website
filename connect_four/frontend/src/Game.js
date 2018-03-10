import React, { Component } from 'react';
import PropTypes from 'prop-types';

import GameBoard from './GameBoard';

import network from './lib/network';

class Game extends Component {

    state = {
        currentGame: null
    }

    createGame = (e) => {
        e.preventDefault();
        network.createGame()
            .then(currentGame => {
                this.setState({currentGame})
            });
    }

    componentDidMount = () => {
        network.fetchGames()
            .then(response => {
                debugger
            })
    }

    render() {
        let {currentGame} = this.state;
        let gameMarkup = currentGame ?
                <GameBoard moves={currentGame.moves} />
                :
                <div>
                    <button onClick={this.createGame}>Start Game</button>
                </div>;

        return (
            <div className="game">
                {gameMarkup}
            </div>
        );
    }
}

export default Game;
