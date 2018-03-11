import math
from connect_four.models import Game, Move

class GameState(object):
    def __init__(self, moves):
        self.moves = moves
        self.children = []

    def populateSuccessors(self):
        # Next player is the 2nd to last player in the moves list
        player_to_move = self.moves[-2:][0].player
        move_dict = {}
        children = []
        #Create dict of current moves so we get O(n) lookup
        for m in self.moves:
            move_dict[m.location] = m

        for i in range(64):
            if i not in move_dict:
                new_move = Move(player=player_to_move, location=i)
                children.append(GameState(self.moves + [new_move]))

        self.children = children


    def utility(self):
        return self.horizontal_utility() + \
               self.vertical_utility()

    def vertical_utility(self):
        u = 1
        columns = {}
        total_scores = {
            1: 0,
            2: 0
        }
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

        for col, col_moves in columns.items():
            prev_player = col_moves[0].player
            prev_location = col_moves[0].location
            score_idx = 1

            scores = {
                1: 2,
                2: 2
            }

            for m in col_moves[1:]:
                curr_score = scores[m.player]
                if m.player == prev_player:
                    if m.location == prev_location + 8:
                        score_idx += 1

                    scores[m.player] = curr_score*math.pow(curr_score, score_idx)
                    prev_location = m.location
                else:
                    curr_player = m.player
                    score_idx = 1
                    scores[m.player] = curr_score*math.pow(curr_score, score_idx)

            for player in scores:
                total_scores[player] += scores[player]

        return total_scores[1] - total_scores[2]


    def horizontal_utility(self):
        u = 1
        rows = {}
        total_scores = {
            1: 0,
            2: 0
        }
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

        for row, row_moves in rows.items():
            prev_player = row_moves[0].player
            prev_location = row_moves[0].location
            score_idx = 1

            scores = {
                1: 2,
                2: 2
            }

            for m in row_moves:
                curr_score = scores[m.player]
                if m.player == prev_player:
                    if m.location == prev_location + 1:
                        score_idx += 1

                    scores[m.player] = curr_score*math.pow(curr_score, score_idx)
                    prev_location = m.location
                else:
                    curr_player = m.player
                    score_idx = 1
                    scores[m.player] = curr_score*math.pow(curr_score, score_idx)

            for player in scores:
                total_scores[player] += scores[player]

        return total_scores[1] - total_scores[2]


    def is_terminal(self):
        return len(self.children) == 0


class AlphaBeta(object):

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
