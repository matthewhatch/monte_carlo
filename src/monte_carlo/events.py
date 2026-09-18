"""Baseball event functions for the Monte Carlo simulator.

Each function accepts the current game state as a 4-element list::

    state = [outs, runner_on_1st, runner_on_2nd, runner_on_3rd]

Runner positions are ``0`` (empty) or ``1`` (occupied).  ``outs`` counts from
0 to 3; the inning ends when it reaches 3.

Every public function returns a ``(new_state, runs_scored)`` tuple where
``new_state`` has the same structure as the input state and ``runs_scored`` is
the number of runs that scored on the play.
"""

import numpy as np
from .constants.events import *

def single(current_state):
    """Simulate a single, randomly choosing a sub-type.

    Sub-types and their probabilities:

    * ``SHORT_SINGLE``  (20%) — runners advance 1 base; runner on 3rd scores.
    * ``MEDIUM_SINGLE`` (50%) — runners on 2nd/3rd score; runner on 1st to 2nd.
    * ``LONG_SINGLE``   (30%) — runners on 2nd/3rd score; runner on 1st to 3rd.

    Args:
        current_state (list[int]): ``[outs, 1st, 2nd, 3rd]``

    Returns:
        tuple[list[int], int]: ``(new_state, runs_scored)``
    """
    types = [SHORT_SINGLE, MEDIUM_SINGLE, LONG_SINGLE]
    probabilities = [.2, .5, .3]
    type = np.random.choice(types, p=probabilities)

    new_state = [current_state[0],0,0,0]
    runs_scored = 0
    
    if type == SHORT_SINGLE:
        new_state, runs_scored = short_single(current_state)

    if type == MEDIUM_SINGLE:
        new_state, runs_scored = medium_single(current_state)
    
    if type == LONG_SINGLE:
        new_state, runs_scored = long_single(current_state)

    return new_state, runs_scored

def short_single(current_state):
    """Handle a short single.

    Runner on 3rd scores.  Runners on 1st and 2nd each advance one base.
    Batter ends up on 1st.

    Args:
        current_state (list[int]): ``[outs, 1st, 2nd, 3rd]``

    Returns:
        tuple[list[int], int]: ``(new_state, runs_scored)``
    """
    new_state = [current_state[0],0,0,0]
    runs_scored = 0

    if current_state[3] == 1:
        runs_scored = runs_scored + 1

    # move runners on 1st and second up 1 base
    new_state[2] = current_state[1]
    new_state[3] = current_state[2]
    new_state[1] = 1

    return new_state, runs_scored

def medium_single(current_state):
    """Handle a medium single.

    Runners on 2nd and 3rd score.  Runner on 1st advances to 2nd.
    Batter ends up on 1st.

    Args:
        current_state (list[int]): ``[outs, 1st, 2nd, 3rd]``

    Returns:
        tuple[list[int], int]: ``(new_state, runs_scored)``
    """
    new_state = [current_state[0],0,0,0]
    runs_scored = 0

    runs_scored = runs_scored + current_state[2] + current_state[3]
    
    new_state[1] = 1
    new_state[2] = current_state[1]
    new_state[3] = 0

    return new_state, runs_scored

def long_single(current_state):
    """Handle a long single.

    Runners on 2nd and 3rd score.  Runner on 1st advances to 3rd.
    Batter ends up on 1st.

    Args:
        current_state (list[int]): ``[outs, 1st, 2nd, 3rd]``

    Returns:
        tuple[list[int], int]: ``(new_state, runs_scored)``
    """
    new_state = [current_state[0],0,0,0]
    runs_scored = 0

    runs_scored = runs_scored + current_state[2] + current_state[3]

    new_state[1] = 1   
    new_state[2] = 0    
    new_state[3] = current_state[1]

    return new_state, runs_scored

def double(current_state):
    """Simulate a double, randomly choosing a sub-type.

    Sub-types and their probabilities:

    * ``SHORT_DOUBLE`` (80%) — batter to 2nd; runner on 1st to 3rd; 2nd/3rd score.
    * ``LONG_DOUBLE``  (20%) — batter to 2nd; all runners score.

    Args:
        current_state (list[int]): ``[outs, 1st, 2nd, 3rd]``

    Returns:
        tuple[list[int], int]: ``(new_state, runs_scored)``
    """
    types = [SHORT_DOUBLE, LONG_DOUBLE]
    probabilities = [.8, .2]
    type = np.random.choice(types, p=probabilities)
    new_state = [current_state[0],0,0,0]
    runs_scored = 0

    if type == SHORT_DOUBLE:
        new_state, runs_scored = short_double(current_state)

    if type == LONG_DOUBLE:
        new_state, runs_scored = long_double(current_state)

    return new_state, runs_scored

def short_double(current_state):
    """Handle a short double.

    Batter ends on 2nd.  Runner on 1st advances to 3rd.
    Runners on 2nd and 3rd score.

    Args:
        current_state (list[int]): ``[outs, 1st, 2nd, 3rd]``

    Returns:
        tuple[list[int], int]: ``(new_state, runs_scored)``
    """
    new_state = [current_state[0],0,0,0]
    runs_scored = 0

    new_state[1] = 0
    new_state[2] = 1
    runs_scored = runs_scored + current_state[2] + current_state[3]
    new_state[3] = current_state[1]
    
    return new_state, runs_scored

def long_double(current_state):
    """Handle a long double.

    Batter ends on 2nd.  All baserunners score.

    Args:
        current_state (list[int]): ``[outs, 1st, 2nd, 3rd]``

    Returns:
        tuple[list[int], int]: ``(new_state, runs_scored)``
    """
    new_state = [current_state[0],0,0,0]
    runs_scored = 0

    new_state[1] = 0
    new_state[2] = 1
    new_state[3] = 0
    runs_scored = runs_scored + current_state[1] + current_state[2] + current_state[3]

    return new_state, runs_scored

def triple(current_state):
    """Handle a triple.

    Batter ends on 3rd.  All baserunners score.

    Args:
        current_state (list[int]): ``[outs, 1st, 2nd, 3rd]``

    Returns:
        tuple[list[int], int]: ``(new_state, runs_scored)``
    """
    new_state = [current_state[0],0,0,0]
    runs_scored = 0
    
    new_state[1] = 0
    new_state[2] = 0
    new_state[3] = 1
    runs_scored = runs_scored + current_state[1] + current_state[2] + current_state[3]

    return new_state, runs_scored

def home_run(current_state):
    """Handle a home run.

    Batter and all baserunners score.  Bases are cleared.

    Args:
        current_state (list[int]): ``[outs, 1st, 2nd, 3rd]``

    Returns:
        tuple[list[int], int]: ``(new_state, runs_scored)``
    """
    new_state = [current_state[0],0,0,0]
    runs_scored = 0

    runs_scored = runs_scored + current_state[1] + current_state[2] + current_state[3] + 1
    new_state = [current_state[0],0,0,0]

    return new_state, runs_scored

def error(current_state):
    """Handle a reached-on-error play.

    Batter reaches 1st.  All existing runners advance one base.
    Runner on 3rd scores.

    Args:
        current_state (list[int]): ``[outs, 1st, 2nd, 3rd]``

    Returns:
        tuple[list[int], int]: ``(new_state, runs_scored)``
    """
    new_state = [current_state[0],1,current_state[1],current_state[2]]
    runs_scored = 0

    runs_scored = runs_scored + current_state[3]

    return new_state, runs_scored

def free_pass(current_state):
    """Handle a walk (BB) or hit-by-pitch (HBP).

    Batter takes 1st base.  Runners are force-advanced only when forced:

    * Runner on 1st only → advances to 2nd.
    * Runners on 1st and 2nd → runner on 2nd advances to 3rd.
    * Bases loaded → runner on 3rd scores (1 run).

    Args:
        current_state (list[int]): ``[outs, 1st, 2nd, 3rd]``

    Returns:
        tuple[list[int], int]: ``(new_state, runs_scored)``
    """
    new_state = [current_state[0], 0,0,0]
    runs_scored = 0

    new_state[1] = 1
    
    if current_state[1] == 1 and current_state[2] == 0 and current_state[3] == 0:
        new_state[2] = current_state[1]
        
    if current_state[1] == 1 and current_state[2] == 1 and current_state[3] == 0:
        new_state[2] == 1
        new_state[3] == 1

    if current_state[1] == 1 and current_state[2] == 0 and current_state[3] == 1:
        new_state[2] = 1
        new_state[3] = 1
    
    if current_state[3] == 1 and current_state[2] == 1 and current_state[1] == 1:
        runs_scored = runs_scored + 1
        new_state[2] = 1
        new_state[3] = 1 

    return new_state, runs_scored

def out_in_play(current_state):
    """Simulate an out in play, dispatching to ground ball or fly ball.

    Out type probabilities (based on real MLB rates):

    * ``GROUND_OUT`` — 53.8%
    * ``LINE_OUT``   — 15.3% (one out added; runners stay)
    * ``FLY_OUT``    — 30.9%

    Args:
        current_state (list[int]): ``[outs, 1st, 2nd, 3rd]``

    Returns:
        tuple[list[int], int]: ``(new_state, runs_scored)``
    """
    types = [GROUND_OUT, LINE_OUT, FLY_OUT]
    probabilities = [.538, .153, .309]
    type = np.random.choice(types, p=probabilities)

    # new_state = [current_state[0], 0,0,0]
    # runs_scored = 0

    if type == FLY_OUT:
        new_state, runs_scored = fly_ball(current_state)
    elif type == GROUND_OUT:
        new_state, runs_scored = ground_ball(current_state)
    elif LINE_OUT:
        # add an out, and players stay
        new_state = [current_state[0] + 1, current_state[1], current_state[2], current_state[3]]
        runs_scored = 0
    
    return new_state, runs_scored

def strike_out(current_state):
    """Handle a strikeout.

    Adds one out.  No runner movement.

    Args:
        current_state (list[int]): ``[outs, 1st, 2nd, 3rd]``

    Returns:
        tuple[list[int], int]: ``([outs+1, same runners], 0)``
    """
    new_state = [current_state[0] + 1, current_state[1], current_state[2], current_state[3]]
    return new_state, 0

def ground_ball(current_state):
    """Simulate a ground ball, dispatching to single out or double play (50/50).

    Args:
        current_state (list[int]): ``[outs, 1st, 2nd, 3rd]``

    Returns:
        tuple[list[int], int]: ``(new_state, runs_scored)``
    """
    types = [GROUND_OUT, GIDP]
    probabilities = [.5, .5]
    type = np.random.choice(types, p=probabilities)

    if type == GROUND_OUT:
        new_state, runs_scored = ground_out(current_state)
    if type == GIDP:
        new_state, runs_scored = gidp(current_state)
    
    return new_state, runs_scored
    
def ground_out(current_state):
    """Handle a standard ground out (one out, possible runner advancement).

    Runner advancement depends on the base configuration:

    * Bases empty — out only.
    * Runner on 1st — runner out at 2nd; batter safe at 1st.
    * Runners on 1st & 2nd — lead runner out at 3rd; batter and trail runner safe.
    * Bases loaded — runner out at home; batter and others safe.
    * Runner on 3rd only — runner scores; bases cleared.
    * Runner on 2nd only — runner advances to 3rd.

    Args:
        current_state (list[int]): ``[outs, 1st, 2nd, 3rd]``

    Returns:
        tuple[list[int], int]: ``(new_state, runs_scored)``
    """
    runs_scored = 0
    outs = current_state[0] + 1
    new_state = [outs, 0, 0, 0]
    
    if new_state[0] == 3:
        return new_state, runs_scored
    
    runners_state = current_state[1:4]

    # if there are no runners on we should do nothing
    if runners_state == [0,0,0]:
        pass

    # if there is a runner on 1st base, that runner is out and the batter is safe at 1st
    if runners_state == [1,0,0]:
        new_state[1] = 1 # batter safe at 1st
        new_state[2] = 0 # runner is out going to 2nd
        new_state[3] = 0

    if runners_state == [1,1,0]:
        # lead runner is out at 3rd, batter safe at 1st and trail runner is safe at 2nd
        new_state[1] = runners_state[0]
        new_state[2] = runners_state[1]
        new_state[3] = 0
    
    if runners_state == [1,1,1]:
        # lead runner is out at home
        new_state[1] = 1
        new_state[2] = 1
        new_state[3] = 1

    if runners_state ==  [0,0,1]:
        # we assume the run will score from 3rd
        runs_scored = runs_scored + 1
        new_state[1] = 0
        new_state[2] = 0
        new_state[3] = 0
    
    if runners_state == [0,1,0]:
        # runner on second advances
        new_state[1] = 0
        new_state[2] = 0
        new_state[3] = 1

    return new_state, runs_scored

def gidp(current_state):
    """Handle a ground-into-double-play (GIDP).

    Two outs are recorded.  Falls back to :func:`ground_out` if there is no
    lead runner or if there are already 0 outs and no runner on 1st.

    Args:
        current_state (list[int]): ``[outs, 1st, 2nd, 3rd]``

    Returns:
        tuple[list[int], int]: ``(new_state, runs_scored)``
    """
    new_state = [current_state[0],0,0,0]
    runs_scored = 0
    runners_state = current_state[1:3]
    
    # if there are no runners there can't be a double play
    if runners_state == [0,0,0]:
        return ground_out(current_state)
    
    if current_state[0] > 0:
        # inning will be over with no runs scored
        new_state[0] = 3
        return new_state, runs_scored
    
    if runners_state in [[1,0,0], [1,1,0]]:
        # lead runners are out
        new_state[0] = new_state[0] + 2
        new_state[3] = 0
        new_state[2] = 0
        new_state[1] = current_state[2]
    
    if runners_state == [1,1,1]:
        # runner scores, batter and runner at 1st going to second is out
        runs_scored = runs_scored + 1
        new_state[0] + 2
        new_state[1] = 0
        new_state[2] = 0
        new_state[3] = 1

    return new_state, runs_scored

def fly_ball(current_state):
    """Simulate a fly ball, dispatching to short, medium, or long sub-type.

    Sub-types and their probabilities:

    * ``SHORT_FLY``  (30%) — one out; no runner advancement.
    * ``MEDIUM_FLY`` (50%) — one out; sac fly possible (runner on 3rd scores if < 2 outs).
    * ``LONG_FLY``   (20%) — one out; sac fly possible; other runners advance.

    Args:
        current_state (list[int]): ``[outs, 1st, 2nd, 3rd]``

    Returns:
        tuple[list[int], int]: ``(new_state, runs_scored)``
    """
    types = [SHORT_FLY, MEDIUM_FLY, LONG_FLY]
    probabilities = [.3, .5, .2]
    type = np.random.choice(types, p=probabilities)
    runs_scored = 0
    new_state = [current_state[0], 0, 0, 0]

    if type == SHORT_FLY:
        new_state, runs_scored = short_fly(current_state)
    
    if type == MEDIUM_FLY:
        new_state, runs_scored = medium_fly(current_state)

    if type == LONG_FLY:
        new_state, runs_scored = long_fly(current_state)
    
    return new_state, runs_scored

def short_fly(current_state):
    """Handle a short fly ball.

    Adds one out.  No runner advancement.

    Args:
        current_state (list[int]): ``[outs, 1st, 2nd, 3rd]``

    Returns:
        tuple[list[int], int]: ``([outs+1, same runners], 0)``
    """
    new_state = [current_state[0], 0,0,0]
    runs_scored = 0

    new_state = [current_state[0] + 1, current_state[1], current_state[2], current_state[3]]
    return new_state, runs_scored

def medium_fly(current_state):
    """Handle a medium fly ball.

    Adds one out.  Runner on 3rd scores if there are fewer than 2 outs
    (sacrifice fly).

    Args:
        current_state (list[int]): ``[outs, 1st, 2nd, 3rd]``

    Returns:
        tuple[list[int], int]: ``(new_state, runs_scored)``
    """
    new_state = [current_state[0], 0,0,0]
    runs_scored = 0

    if current_state[3] == 1 and current_state[0] < 2:
        runs_scored = runs_scored + 1
        new_state[3] = 0
    
    new_state[0] = current_state[0] + 1
    new_state[1] = current_state[1]
    new_state[2] = current_state[2]

    return new_state, runs_scored

def long_fly(current_state):
    """Handle a long fly ball.

    Adds one out.  Runner on 3rd scores if there are fewer than 2 outs
    (sacrifice fly).  Remaining runners each advance one base.

    Args:
        current_state (list[int]): ``[outs, 1st, 2nd, 3rd]``

    Returns:
        tuple[list[int], int]: ``(new_state, runs_scored)``
    """
    new_state = [current_state[0], 0,0,0]
    runs_scored = 0

    if current_state[3] == 1 and current_state[0] < 2:
        runs_scored = runs_scored + 1

    new_state[1] = 0
    new_state[2] = current_state[1]
    new_state[3] = current_state[2]

    return new_state, runs_scored    
