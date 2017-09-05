"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score_2(game, player):
    """Outputs a score equal to square of the distance from the position
    under evaluation and the opponent player.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : hashable
        One of the objects registered by the game object as a valid player.
        (i.e., `player` should be either game.__player_1__ or
        game.__player_2__).

    Returns
    ----------
    float
        The heuristic value of the current game state
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    yp, xp = game.get_player_location(player)
    yo, xo = game.get_player_location(game.get_opponent(player))
    return float((yp - yo)**2 + (xp - xo)**2)


def custom_score(game, player):
    """Outputs a score equal to square of the distance from the center 
    of the board (higher distance gets lower values, int he contrary of
    the provided AB_Center heuristic function) and the player weighted 
    with the difference between player's and opponent's number of legal 
    moves.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : hashable
        One of the objects registered by the game object as a valid player.
        (i.e., `player` should be either game.__player_1__ or
        game.__player_2__).

    Returns
    ----------
    float
        The heuristic value of the current game state
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")
    k = game.width / 2.
    w, h = game.width / 2., game.height / 2.
    y, x = game.get_player_location(player)
    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    return k * float(own_moves - opp_moves) - float((h - y)**2 + (w - x)**2)


def custom_score_3(game, player):
    """Outputs a score equal to square of the distance from the position 
    under evaluation and the opponent weighted with the difference between
    player's and opponent's number of legal moves.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : hashable
        One of the objects registered by the game object as a valid player.
        (i.e., `player` should be either game.__player_1__ or
        game.__player_2__).

    Returns
    ----------
    float
        The heuristic value of the current game state
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")
    k = game.width / 2.
    yp, xp = game.get_player_location(player)
    yo, xo = game.get_player_location(game.get_opponent(player))
    own_moves = len(game.get_legal_moves(player))
    return k * float(own_moves) + float((yp - yo)**2 + (xp - xo)**2)


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        super().__init__()
        self.score = score_fn

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        legal_moves = game.get_legal_moves()
        best_move = (legal_moves[0] if legal_moves else (-1, -1))

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            best_move = self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move


    def _min_value(self, game, depth):
        '''
        Implements the min_value recursive evaluation in the minimax algorithm

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        depth : int
            A strictly positive integer (i.e., 1, 2, 3,...) for the number of
            layers in the game tree to explore for fixed-depth search. (i.e., a
            depth of one (1) would only explore the immediate sucessors of the
            current state.)

        Returns
        ----------
        float
            Returns the min value among the evaluated legal moves
        '''
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        if depth <= 0:
            return self.score(game, self)
        min_val = float("inf")
        legal_moves = game.get_legal_moves()
        for m in legal_moves:
            score = self._max_value(game.forecast_move(m), depth - 1)
            if score < min_val:
                min_val = score
        return min_val


    def _max_value(self, game, depth):
        '''
        Implements the max_value recursive evaluation in the minimax algorithm

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        depth : int
            A strictly positive integer (i.e., 1, 2, 3,...) for the number of
            layers in the game tree to explore for fixed-depth search. (i.e., a
            depth of one (1) would only explore the immediate sucessors of the
            current state.)

        Returns
        ----------
        float
            Returns the max value among the evaluated legal moves
        '''
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        if depth <= 0:
            return self.score(game, self)
        max_val = float("-inf")
        legal_moves = game.get_legal_moves()
        for m in legal_moves:
            score = self._min_value(game.forecast_move(m), depth - 1)
            if score > max_val:
                max_val = score
        return max_val


    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return(-1, -1)
        final_move = (legal_moves[0] if legal_moves else (-1, -1))
        max_val = float("-inf")
        for m in legal_moves:
            score = self._min_value(game.forecast_move(m), depth - 1)
            if score > max_val:
                final_move = m
                max_val = score
        return final_move


class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        super().__init__()
        self.score = score_fn


    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        legal_moves = game.get_legal_moves()
        best_move = (legal_moves[0] if legal_moves else (-1, -1))
        partial_depth = 1

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            while True:
                best_move = self.alphabeta(game, partial_depth)
                partial_depth += 1

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move


    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < 3 * self.TIMER_THRESHOLD:
            raise SearchTimeout()

        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return(-1, -1)
        final_move = (legal_moves[0] if legal_moves else (-1, -1))
        max_val = float("-inf")
        for m in legal_moves:
            score = self._min_value(game.forecast_move(m), depth - 1, alpha, beta)
            if score > max_val:
                final_move = m
                max_val = score
            if max_val >= beta:
                return final_move
            alpha = max(alpha, max_val)
        return final_move 


    def _min_value(self, game, depth, alpha, beta):
        '''
        Implements the min_value recursive evaluation in the alpha-beta 
        pruning algorithm

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        depth : int
            A strictly positive integer (i.e., 1, 2, 3,...) for the number of
            layers in the game tree to explore for fixed-depth search. (i.e., a
            depth of one (1) would only explore the immediate sucessors of the
            current state.)

        Returns
        ----------
        float
            Returns the min value among the evaluated legal moves
        '''
        if self.time_left() < 3 * self.TIMER_THRESHOLD:
            raise SearchTimeout()
        if depth <= 0:
            return self.score(game, self)
        min_val = float("inf")
        legal_moves = game.get_legal_moves()
        for m in legal_moves:
            score = self._max_value(game.forecast_move(m), depth - 1, alpha, beta)
            if score < min_val:
                min_val = score
            if min_val <= alpha:
                return min_val
            beta = min(beta, min_val)
        return min_val


    def _max_value(self, game, depth, alpha, beta):
        '''
        Implements the max_value recursive evaluation in the alpha-beta 
        pruning algorithm

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        depth : int
            A strictly positive integer (i.e., 1, 2, 3,...) for the number of
            layers in the game tree to explore for fixed-depth search. (i.e., a
            depth of one (1) would only explore the immediate sucessors of the
            current state.)

        Returns
        ----------
        float
            Returns the max value among the evaluated legal moves
        '''
        if self.time_left() < 3 * self.TIMER_THRESHOLD:
            raise SearchTimeout()
        if depth <= 0:
            return self.score(game, self)
        max_val = float("-inf")
        legal_moves = game.get_legal_moves()
        for m in legal_moves:
            score = self._min_value(game.forecast_move(m), depth - 1, alpha, beta)
            if score > max_val:
                max_val = score
            if max_val >= beta:
                return max_val
            alpha = max(alpha, max_val)
        return max_val
