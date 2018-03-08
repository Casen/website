import React, { Component } from 'react';
import PropTypes from 'prop-types';


class BoardSpace extends Component {
    static propTypes = {
        index: PropTypes.number.isRequired
    }

    makeMove = (e) => {
        console.log('you clicked ', this.props.index);
    }

    render() {
        var styles = {
            float: 'left',
            margin: '2px',
            width: '48px',
            textAlign: 'center',
            cursor: 'pointer',
            backgroundColor: '#cccccc'
        };

        return (
            <div className="board-space" style={styles} onClick={this.makeMove}>
                <p>{this.props.index}</p>
            </div>
        );
    }
}

class GameBoard extends Component {
    render() {
        var styles = {
            width: '450px',
            margin: '50px auto',
        };

        var boardSpaces = [];
        for (var i=0; i<64; i++) {
            boardSpaces.push(<BoardSpace index={i} key={'board-space-' + i}/>);
        }
        return (
            <div className="game-board" style={styles}>
                {boardSpaces}
            </div>
        );
    }
}

export default GameBoard;
