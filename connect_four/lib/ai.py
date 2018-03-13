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
        if len(self.current_state.moves) < 3:
            return self.make_opening_move()

        # If opponent can with in one move, we make that move to block
        losing_move = self.find_losing_move()
        if losing_move:
            return self.return_next_state(losing_move)

        # If we can win in one move, we make that move to finish
        winning_move = self.find_winning_move()
        if winning_move:
            return self.return_next_state(winning_move)

        #If we've exhausted other options, do an AB search
        return self.ai.search(self.current_state, maximizing_player=self.player == 1)


    def find_losing_move(self):
        self.current_state.utility()
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

class GameState(object):
    """Represents the state of a single game board position"""
    def __init__(self, moves, move_made=None):
        self.moves = moves

        # If gamestate was created by making a new move, capture it here for use later
        if move_made:
            self.moves = self.moves + [move_made]
            self.move_made = move_made

        self.moves_dict = {}
        #Create dict of current moves so we get O(n) lookup
        for m in self.moves:
            self.moves_dict[m.location] = m

        self.col_moves = self.group_moves_by_column()
        self.row_moves = self.group_moves_by_row()

        self.children = []

        #Keep track of max consecutive moves achieved for each player
        self.consec_moves = {
            'horizontal': {
                1: 0,
                2: 0
            },
            'vertical': {
                1: 0,
                2: 0
            }
        }

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

    def reset_consec_moves(self):
        self.consec_moves = {
            'horizontal': {
                1: 0,
                2: 0
            },
            'vertical': {
                1: 0,
                2: 0
            }
        }

    def update_consecutive_count(self, player, direction): 
        self.consec_moves[direction][player] += 1

    def get_consecutive_count(self, player, direction): 
        return self.consec_moves[direction][player]

    def player_one_wins(self):
        vc = self.get_consecutive_count(1, 'vertical')
        hc = self.get_consecutive_count(1, 'horizontal')
        return hc == 4 or vc == 4

    def player_two_wins(self):
        vc = self.get_consecutive_count(2, 'vertical')
        hc = self.get_consecutive_count(2, 'horizontal')
        return hc == 4 or vc == 4

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
        self.reset_consecutive_count()

        infinity = float('inf')
        util_calc = self.horizontal_utility() + \
                    self.vertical_utility()

        if self.player_one_wins():
            return infinity

        if self.player_two_wins():
            return -infinity

        return util_calc


    def vertical_utility(self):
        u = 1
        total_scores = {
            1: 0,
            2: 0
        }

        for col, self.col_moves in columns.items():
            prev_player = None
            prev_location = None
            score_idx = 1
            print("operating on column %d" % col)

            scores = {
                1: 0,
                2: 0
            }

            for m in col_moves:
                curr_score = scores[m.player]
                if not prev_player:
                    print("player %d has first move in col" % m.player)
                    prev_player = m.player
                    prev_location = m.location
                    scores[m.player] = 2
                elif m.player == prev_player:
                    print("player %d has another move in col" % m.player)
                    print("location %d" % m.location)
                    if m.location == prev_location + 8:
                        print("player %d has consecutive move" % m.player)

                        #Update current consecutive count for the game so far
                        self.update_consecutive_count(m.player)
                        scores[m.player] = curr_score * math.pow(curr_score, 4)
                    else:
                        scores[m.player] = curr_score + 2

                    print("player has new score: %d" % scores[m.player])
                    prev_location = m.location
                else:
                    print("switching to player %d and resetting score_idx" % m.player)
                    print("location %d" % m.location)
                    prev_player = m.player
                    prev_location = m.location
                    score_idx = 1

                    scores[m.player] = curr_score + 2 if curr_score else 2
                    print("player has new score: %d" % scores[m.player])

            for player in scores:
                total_scores[player] += scores[player]

            print("current total scores")
            print(total_scores)

        return total_scores[1] - total_scores[2]


    def horizontal_utility(self):
        u = 1
        total_scores = {
            1: 0,
            2: 0
        }

        for row, self.row_moves in rows.items():
            prev_player = None
            prev_location = None
            score_idx = 1
            print("operating on row %d" % row)

            scores = {
                1: 0,
                2: 0
            }

            for m in row_moves:
                curr_score = scores[m.player]
                if not prev_player:
                    print("player %d has first move in row" % m.player)
                    prev_player = m.player
                    prev_location = m.location
                    scores[m.player] = 2
                    print("player has new score: %d" % scores[m.player])
                elif m.player == prev_player:
                    print("player %d has another move in row" % m.player)
                    print("location %d" % m.location)

                    if m.location == prev_location + 1:
                        print("player %d has consecutive move in row" % m.player)

                        #Update current consecutive count for the game so far
                        self.update_consecutive_count(m.player)
                        scores[m.player] = curr_score * math.pow(curr_score, 4)
                    else:
                        scores[m.player] = curr_score + 2

                    print("player has new score: %d" % scores[m.player])
                    prev_location = m.location
                else:
                    print("switching to player %d and resetting score_idx" % m.player)
                    print("location %d" % m.location)
                    prev_player = m.player
                    prev_location = m.location
                    score_idx = 1

                    scores[m.player] = curr_score + 2 if curr_score else 2
                    print("player has new score: %d" % scores[m.player])

            for player in scores:
                total_scores[player] += scores[player]

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



    def min_value(self, node, alpha, beta):
        if node.is_terminal():
            return node.utility()

        infinity = float('inf')
        value = infinity

        successors = self.get_successors(node)
        for child in successors:
            value = min(value, self.max_value(child, alpha, beta))
            if value <= alpha:
                return value
            beta = min(beta, value)
        return value

    def max_value(self, node, alpha, beta):
        if node.is_terminal():
            return node.utility()

        infinity = float('inf')
        value = -infinity

        successors = node.successors()
        for child in successors:
            value = max(value, self.min_value(child, alpha, beta))
            if value >= beta:
                return value

            alpha = max(alpha, value)
        return value
