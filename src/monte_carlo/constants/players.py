"""Pre-defined player stat dictionaries for testing and offline use.

Each constant is a dictionary whose keys match the constructor parameters of
:class:`~monte_carlo.classes.Player.Player`.  These can be used directly
without a CSV file or network access.

Available constants
-------------------
TROUT16 : Mike Trout's 2016 season statistics.
"""

TROUT16 = {
    "plate_appearences": 681,
    "at_bats": 554,
    "errors": 10,
    "outs": 234,
    "strike_outs": 137,
    "walks":  118,
    "hbp": 11,
    "singles": 107,
    "doubles": 32,
    "triples": 5,
    "home_runs": 29
}
