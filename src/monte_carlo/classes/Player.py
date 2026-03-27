"""Player model for the Monte Carlo baseball simulator.

The :class:`Player` class converts raw seasonal statistics into a probability
distribution over plate appearance outcomes and drives the at-bat simulation.
"""

import numpy as np
import pandas as pd
from ..events import *
from ..constants.events import *

class Player():
    """Probability model for a single MLB batter.

    Converts raw seasonal statistics into per-plate-appearance probabilities
    and simulates individual at-bats using :mod:`numpy.random`.

    Attributes:
        plate_appearences (int): Total plate appearances.
        at_bats (int): Official at-bats.
        errors (int): Times reached on error.
        p_error (float): Probability of reaching on error.
        outs (int): Outs recorded (not including strikeouts).
        p_out (float): Probability of an out in play.
        strike_outs (int): Strikeouts.
        p_strike_out (float): Probability of a strikeout.
        walks (int): Base on balls.
        p_walk (float): Probability of a walk.
        hbp (int): Hit by pitch.
        p_hbp (float): Probability of hit by pitch.
        singles (int): Singles.
        p_single (float): Probability of a single.
        doubles (int): Doubles.
        p_double (float): Probability of a double.
        triples (int): Triples.
        p_triple (float): Probability of a triple.
        home_runs (int): Home runs.
        p_home_run (float): Probability of a home run.
        runs_created (float): Set after simulation via :meth:`runs_created`.
    """

    def __init__(
            self,
            plate_appearences,
            at_bats,
            errors,
            outs,
            strike_outs,
            walks,
            hbp,
            singles,
            doubles,
            triples,
            home_runs
    ) -> None:
        """Initialize a Player from raw seasonal statistics.

        Args:
            plate_appearences (int): Total plate appearances in the season.
            at_bats (int): Official at-bats.
            errors (int): Times reached on error.
            outs (int): Outs recorded (excluding strikeouts).
            strike_outs (int): Strikeouts.
            walks (int): Base on balls.
            hbp (int): Hit by pitch.
            singles (int): Singles.
            doubles (int): Doubles.
            triples (int): Triples.
            home_runs (int): Home runs.
        """
        self.plate_appearences = plate_appearences
        self.at_bats = at_bats
        self.errors = errors
        self.p_error = errors / plate_appearences
        self.outs = outs
        self.p_out = outs / plate_appearences
        self.strike_outs = strike_outs
        self.p_strike_out = strike_outs / plate_appearences
        self.walks = walks
        self.p_walk = walks / plate_appearences
        self.hbp = hbp
        self.p_hbp = hbp / plate_appearences
        self.singles = singles
        self.p_single = singles / plate_appearences
        self.doubles = doubles
        self.p_double = doubles / plate_appearences
        self.triples = triples
        self.p_triple = triples / plate_appearences
        self.home_runs = home_runs
        self.p_home_run = home_runs / plate_appearences
    
    def normalize_probabilites(self, probabilities):
        """Normalize a list of probabilities so they sum to exactly 1.0.

        Guards against floating-point drift before passing to
        ``numpy.random.choice``.

        Args:
            probabilities (list[float]): Raw probability values.

        Returns:
            list[float]: Normalized probabilities that sum to 1.0.
        """
        return [p / total_prob for p in probabilities]
    
    def runs_created(self, rc):
        """Get or set the Runs Created value.

        Args:
            rc (float | None): Average runs per game from simulation.
                Pass ``None`` to read the current stored value.

        Returns:
            float | None: The stored ``runs_created`` value when ``rc`` is
            ``None``; otherwise ``None`` (the value is stored on the instance).
        """
        if rc == None:
            return self.runs_created
        
        self.runs_created = rc
    
    def simulate_ab(self, current_state):
        """Simulate a single plate appearance and update the game state.

        Draws one outcome from the player's probability distribution using
        ``numpy.random.choice``, then delegates to the appropriate event
        function in :mod:`~monte_carlo.events`.

        Args:
            current_state (list[int]): ``[outs, runner_1st, runner_2nd, runner_3rd]``
                where each runner position is 0 (empty) or 1 (occupied).

        Returns:
            tuple[list[int], int]: ``(new_state, runs_scored)`` where
            ``new_state`` has the same structure as ``current_state``.
        """
        new_state = [current_state[0],0,0,0]
        runs_scored = 0

        outcomes = [ERROR, OUT, K, BB, HBP, SINGLE, DOUBLE, TRIPLE, HOME_RUN]
        probabilities = self.normalize_probabilites([self.p_error, self.p_out, self.p_strike_out, self.p_walk, self.p_hbp, self.p_single, self.p_double, self.p_triple, self.p_home_run])
        outcome = np.random.choice(outcomes, p=probabilities)

        if outcome == HOME_RUN:
            new_state, runs_scored = home_run(current_state)
        elif outcome == TRIPLE:
            new_state, runs_scored = triple(current_state)
        elif outcome == DOUBLE:
            new_state, runs_scored = double(current_state)
        elif outcome == ERROR:
            new_state, runs_scored = error(current_state)
        elif outcome == BB or outcome == HBP:
            new_state, runs_scored = free_pass(current_state)
        elif outcome == SINGLE:
            new_state, runs_scored = single(current_state)
        elif outcome == K:
            new_state, runs_scored = strike_out(current_state)
        elif outcome == OUT:
            new_state, runs_scored = out_in_play(current_state)
        else:
            new_state = current_state

        return new_state, runs_scored
    
    def __str__(self) -> str:
        """Return a formatted table of the player's raw statistics.

        Probability columns (those prefixed with ``p_``) are excluded for
        readability.

        Returns:
            str: A single-row ``pandas.DataFrame`` string representation.
        """
        player_df = pd.DataFrame(self.__dict__, index=[0])
        # only return columns that don't start with 'p_'
        player_df = player_df.drop(player_df.filter(regex='p_').columns, axis=1)
        return player_df.to_string(index=False)