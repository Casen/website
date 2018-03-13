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
                this.setState({currentGame});
            });
    }

    componentDidMount = () => {
        network.fetchGame(1)
            .then(currentGame => {
                console.log('fetched the game ', currentGame);
                this.setState({currentGame});
            });
    }

    persistMove = (move) => {
        network.makeMove(move)
            .then(persistedMove => {

                //Once we've persisted the move, let's ask the AI for it's move
                network.getAiMove(move)
                    .then(updatedGame => {
                        this.setState({currentGame: updatedGame});
                    });
            });
    }

    render() {
        let {currentGame} = this.state;
        let gameMarkup = currentGame ?
                <GameBoard game={currentGame} persistMove={this.persistMove}/>
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
