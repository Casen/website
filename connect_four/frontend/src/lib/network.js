const BASE_URL = 'http://localhost:8000';

class Network {

    post(url, payload={}) {
        return fetch(url, {
            method: 'POST',
            body: JSON.stringify(payload),
            headers: new Headers({
                'Content-Type': 'application/json'
            })
        })
        .then(res => {
            return res.json();
        })
        .catch(error => console.error(error));
    }

    createGame() {
        let url = BASE_URL + '/connect_four/games/';
        return this.post(url);
    }

    makeMove(move) {
        let url = BASE_URL + '/connect_four/games/' + move.game + '/moves/';
        return this.post(url, move);
    }

    getAiMove(move) {
        let url = BASE_URL + '/connect_four/games/'+ move.game + '/ai_move/';
        return this.post(url, move);
    }

    fetchGames() {
        let url = BASE_URL + '/connect_four/games/';
        return fetch(url).then(res => {
                    return res.json();
                })
                .catch(error => console.error(error));
    }

    fetchGame(gameId) {
        let url = BASE_URL + '/connect_four/games/' + gameId;
        return fetch(url).then(res => {
            return res.json();
        })
        .catch(error => console.error(error));
    }
}

export default new Network();
