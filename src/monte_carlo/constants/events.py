"""String constants for all plate appearance outcome types.

These constants are used throughout :mod:`~monte_carlo.events` and
:class:`~monte_carlo.classes.Player.Player` to identify event types in a
readable, refactor-safe way.

Primary outcomes
----------------
HOME_RUN, TRIPLE, DOUBLE, SINGLE, BB (walk), HBP, K (strikeout), OUT, ERROR

Single sub-types
----------------
SHORT_SINGLE, MEDIUM_SINGLE, LONG_SINGLE

Double sub-types
----------------
SHORT_DOUBLE, LONG_DOUBLE

Out sub-types
-------------
GROUND_OUT, LINE_OUT, FLY_OUT, GIDP, SHORT_FLY, MEDIUM_FLY, LONG_FLY
"""


HOME_RUN = 'HOME_RUN'
TRIPLE = 'TRIPLE'
DOUBLE = 'DOUBLE'
ERROR = 'ERROR'
BB = 'WALK'
SINGLE = 'SINGLE'
K = 'STRIKE_OUT'
OUT = 'OUT'
HBP = 'HBP'

SHORT_SINGLE = 'SHORT_SINGLE'
MEDIUM_SINGLE = 'MEDIUM_SINGLE'
LONG_SINGLE = 'LONG_SINGLE'
SHORT_DOUBLE = 'SHORT_DOUBLE'
LONG_DOUBLE = 'LONG_DOUBLE'
GROUND_OUT = 'GROUND_OUT'
LINE_OUT = 'LINE_OUT'
FLY_OUT = 'FLY_OUT'
GIDP = 'GIDP'
SHORT_FLY = 'SHORT_FLY'
MEDIUM_FLY = 'MEDIUM_FLY'
LONG_FLY = 'LONG_FLY'