/*jshint loopfunc: true */
import React, { Component } from 'react';
import PropTypes from 'prop-types';


class BoardSpace extends Component {
    static propTypes = {
        index: PropTypes.number.isRequired,
        makeMove: PropTypes.func.isRequired,
        move: PropTypes.object
    }


    clickSpace = (e) => {
        e.preventDefault();
        this.props.makeMove(this.props.index);
    }

    render() {
        var placeholder = !this.props.move;
        var move = placeholder ? "p" : this.props.move;
        var style = placeholder ? {visibility:"hidden"} : {};
        var moveChar = move.player === 1 ? 'x': 'o';
        return (
            <div className="board-space" onClick={this.clickSpace}>
                <p style={style}>{moveChar}</p>
            </div>
        );
    }
}

class GameBoard extends Component {

    static propTypes = {
        persistMove: PropTypes.func.isRequired,
        game: PropTypes.object
    }

    static defaultProps = {
        game: {ai_starts: false, moves: []}
    }

    state = {
        isPlayerOne: !this.props.game.ai_starts,
        game: this.props.game
    }

    makeMove = (spaceIndex) => {
        let {game, isPlayerOne} = this.state;
        let move = {
            game: game.id,
            player: isPlayerOne ? 1 : 2,
            location: spaceIndex
        };

        game.moves.push(move);
        this.setState({game});

        // Make sure move state is persisted out of band
        this.props.persistMove(move);
    }

    componentWillReceiveProps = (nextProps) => {
        let state = this.state;
        let currgame = this.props.game;
        let move_made = currgame.moves.length !== nextProps.game.moves.length;
        let game_ended = currgame.winner !== nextProps.game.winner;
        if (move_made || game_ended) {
            state.game = nextProps.game;
            this.setState(state);
        }
    }

    renderBoardSpaces = () => {
        var boardSpaces = [];
        var {game} = this.state;
        for (var i=0; i<64; i++) {
            // eslint-disable-next-line
            let move = game.moves.find(move => move.location === i);
            boardSpaces.push(<BoardSpace index={i} move={move} makeMove={this.makeMove} key={'board-space-' + i}/>);
        }

        return boardSpaces;
    }

    render() {
        var {game} = this.state;
        return (
            <div className="game-board">
                {game.winner ? <h1>Player {game.winner} wins!</h1> : null}
                {this.renderBoardSpaces()}
            </div>
        );
    }
}

export default GameBoard;
