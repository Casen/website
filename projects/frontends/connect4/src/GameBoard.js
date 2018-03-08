import React, { Component } from 'react';
import PropTypes from 'prop-types';


class BoardSpace extends Component {
    static propTypes = {
        index: PropTypes.number.isRequired,
        makeMove: PropTypes.func.isRequired,
        move: PropTypes.string
    }

    clickSpace = (e) => {
        e.preventDefault();
        this.props.makeMove(this.props.index);
    }

    render() {
        var placeholder = !this.props.move;
        var move = placeholder ? "p" : this.props.move;
        var style = placeholder ? {visibility:"hidden"} : {};
        return (
            <div className="board-space" onClick={this.clickSpace}>
                <p style={style}>{move}</p>
            </div>
        );
    }
}

class GameBoard extends Component {

    state = {
        isPlayerOne: true,
        moves: {}
    }

    makeMove = (spaceIndex) => {
        let update = this.state || {};
        update[spaceIndex] = "";

        if (this.state.isPlayerOne) {
            update[spaceIndex] = "x";
        } else {
            update[spaceIndex] = "o";
        }

        this.setState({moves: update});
    }

    render() {
        var boardSpaces = [];
        for (var i=0; i<64; i++) {
            let move = this.state.moves[i];
            boardSpaces.push(<BoardSpace index={i} move={move} makeMove={this.makeMove} key={'board-space-' + i}/>);
        }
        return (
            <div className="game-board">
                {boardSpaces}
            </div>
        );
    }
}

export default GameBoard;
