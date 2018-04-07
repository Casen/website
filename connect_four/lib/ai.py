import math
from connect_four.models import Game, Move

class GameSession(object):
    """
    General heuristics and higher level reasoning about the game
    """
    def __init__(self, game):
        self.ai = GameAI()
        self.game = game
        self.player = 1 if game.ai_starts else 2
        self.opponent = 2 if self.player == 1 else 1
        self.current_state = GameState(self.game.to_state())

    def make_move(self):
        self.current_state.utility()

        #If the opponent has already won, no point in making a move!
        if self.current_state.player_wins(self.opponent):
            return self.current_state

        if len(self.current_state.moves) < 3:
            return self.make_opening_move()

        # If opponent can win shortly, let's try to block
        blocking_move = self.find_blocking_move()
        if blocking_move:
            return self.return_next_state(blocking_move)

        # If we can win in one move, we make that move to finish
        winning_move = self.find_winning_move()
        if winning_move:
            return self.return_next_state(winning_move)

        #If we've exhausted other options, do an AB search
        return self.ai.search(self.current_state, maximizing_player=self.player == 1)


    def find_blocking_move(self):
        opp_seq = self.current_state.find_sequence(self.opponent, 2)

        if opp_seq:
            for l in opp_seq.blocking_locations():
                if not self.current_state.move_played(l):
                    return l

        return None


    def find_winning_move(self):
        return None

    def make_opening_move(self):
        center_positions = [27, 28, 35, 36]
        for p in center_positions:
            if not self.current_state.move_played(p):
                return self.return_next_state(p)

    def return_next_state(self, move):
        new_move = Move(player=self.player, location=move)
        return GameState(self.current_state.moves, move_made=new_move)

class MoveSequence(object):
    """Represents a consecutive sequence of moves in a given board state"""

    def __init__(self, moves, orientation):
        self.moves = moves
        self.orientation = orientation

    def is_win(self):
        return len(self.moves) == 4

    def has_length(self, length):
        return len(self.moves) == length

    def blocking_locations(self):
        first = self.moves[0]
        last = self.moves[-1]
        if self.orientation == 'v':
            return [first - 8, last + 8]
        else:
            return [first - 1, last + 1]


class GameState(object):
    """Represents the state of a single game board position"""
    def __init__(self, moves, move_made=None):
        self.moves = moves

        # If gamestate was created by making a new move, capture it here for use later
        if move_made:
            self.moves = self.moves + [move_made]
            self.move_made = move_made

        #Create dict of current moves so we get O(n) lookup
        self.moves_dict = {}
        for m in self.moves:
            self.moves_dict[m.location] = m

        #Create dicts of moves grouped into columns and rows for utility comps
        self.col_moves = self.group_moves_by_column()
        self.row_moves = self.group_moves_by_row()

        #Keep track of max consecutive moves achieved for each player
        self.reset_move_sequences()

        self.children = []
        self.winning_player = None


    def move_played(self, move_location):
        return move_location in self.moves_dict


    def populateSuccessors(self):
        # If num moves made is even, it's player one's turn
        player_to_move = 1 if len(self.moves) % 2 == 0 else 2
        children = []

        for i in range(64):
            if i not in self.moves_dict:
                new_move = Move(player=player_to_move, location=i)
                children.append(GameState(self.moves, move_made=new_move))

        self.children = children


    def reset_move_sequences(self):
        self.player_move_sequences = {
            1: [],
            2: []
        }


    def find_sequence(self, player, seq_length):
        player_seqs = self.player_move_sequences[player]
        for s in player_seqs:
            if s.has_length(seq_length):
                return s


    def capture_move_sequences(self, player, sequences):
        curr_sequences = self.player_move_sequences[player]
        self.player_move_sequences[player] = curr_sequences + sequences
        print("sequences captured for player %d" % player)
        print(self.player_move_sequences[player])


    def player_wins(self, player):
        for s in self.player_move_sequences[player]:
            if s.is_win():
                self.winning_player = player
                return True


    def group_moves_by_column(self):
        columns = {}
        #duplicate the moves array so we can sort it by location
        moves = self.moves + []
        moves.sort(key=lambda move: move.location)

        # Gather moves into columns
        for m in moves:
            col = (m.location % 8) + 1
            if col in columns:
                columns[col].append(m)
            else:
                columns[col] = [m]

        return columns


    def group_moves_by_row(self):
        rows = {}
        #duplicate the moves array so we can sort it by location
        moves = self.moves + []
        moves.sort(key=lambda move: move.location)

        # Gather moves into rows
        for m in moves:
            row = int(m.location/8) + 1
            if row in rows:
                rows[row].append(m)
            else:
                rows[row] = [m]

        return rows


    def utility(self):
        self.reset_move_sequences()

        infinity = float('inf')
        consec_in_col = lambda prev_loc, loc: loc == prev_loc+8
        consec_in_row = lambda prev_loc, loc: loc == prev_loc+1
        util_calc = self.utility_for_orientation(self.col_moves, consec_in_col, 'v') + \
                    self.utility_for_orientation(self.row_moves, consec_in_row, 'h')

        if self.player_wins(1):
            print('player one wins!')
            return infinity

        if self.player_wins(2):
            print('player two wins!')
            return -infinity

        return util_calc


    def utility_for_orientation(self, oriented_moves, is_consecutive, orientation):
        total_scores = {
            1: 0,
            2: 0
        }

        for group, moves in oriented_moves.items():
            prev_player = None
            prev_location = None
            curr_move_sequence = {
                1: [],
                2: []
            }
            score_idx = 1
            print("operating on group %d" % group)

            scores = {
                1: 0,
                2: 0
            }

            move_sequences = {
                1: [],
                2: []
            }

            for m in moves:
                curr_score = scores[m.player]
                if not prev_player:
                    print("player %d has first move in group" % m.player)
                    prev_player = m.player
                    prev_location = m.location
                    scores[m.player] = 2
                    curr_move_sequence[m.player].append(m.location)
                elif m.player == prev_player:
                    print("player %d has another move in group" % m.player)
                    print("location %d" % m.location)
                    if is_consecutive(prev_location, m.location):
                        print("player %d has consecutive move" % m.player)

                        curr_move_sequence[m.player].append(m.location)
                        print(curr_move_sequence[m.player])
                        scores[m.player] = curr_score * math.pow(curr_score, 2)
                    else:
                        scores[m.player] = curr_score + 2

                    print("player has new score: %d" % scores[m.player])
                    prev_location = m.location
                else:
                    print("switching to player %d and resetting score_idx" % m.player)
                    print("location %d" % m.location)

                    if len(curr_move_sequence[prev_player]) > 1:
                        print("found a sequence")
                        move_sequences[prev_player].append(MoveSequence(curr_move_sequence[prev_player], orientation))
                        print(move_sequences)
                        curr_move_sequence[prev_player] = []

                    prev_player = m.player
                    prev_location = m.location
                    score_idx = 1

                    scores[m.player] = curr_score + 2 if curr_score else 2
                    print("player has new score: %d" % scores[m.player])

            #Tally up the total scores
            for player in scores:
                total_scores[player] += scores[player]

            #Capture remaining move sequences from last run
            for player, sequence in curr_move_sequence.items():
                if len(sequence) > 1:
                    move_sequences[player].append(MoveSequence(sequence, orientation))

            #Persist all move sequences that were found
            for player, sequences in move_sequences.items():
                if len(sequences):
                    self.capture_move_sequences(m.player, sequences)

            print("current total scores")
            print(total_scores)

        return total_scores[1] - total_scores[2]



    def is_terminal(self):
        return len(self.children) == 0


class GameAI(object):

    def search(self, node, depth=10000000, maximizing_player=False):
        infinity = float('inf')
        alpha = -infinity
        beta = infinity
        next_state = None
        node.populateSuccessors()

        for child in node.children:
            child.score = self.ab_search(child, depth, alpha, beta, maximizing_player)

        node.children.sort(key=lambda child: child.score)

        if maximizing_player:
            return node.children[-1:][0]
        else:
            return node.children[0]

    def ab_search(self, node, depth, alpha, beta, maximizing_player):
        if depth == 0 or node.is_terminal():
            print("hit the bottom")
            return node.utility()

        infinity = float('inf')
        if maximizing_player:
            val = -infinity
            node.populateSuccessors()
            for child in node.children:
                val = max(val, self.ab_search(child, depth-1, alpha, beta, False))
                alpha = max(alpha, val)

                if beta <= alpha:
                    break

            return val
        else:
            val = infinity
            node.populateSuccessors()
            for child in node.children:
                val = min(val, self.ab_search(child, depth-1, alpha, beta, True))
                beta = min(beta, val)
                if beta <= alpha:
                    break

            return val
