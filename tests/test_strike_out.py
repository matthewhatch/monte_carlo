import unittest
from monte_carlo.events import strike_out

class TestStrikeOut(unittest.TestCase):
    def test_strike_out(self):
        current_state = [0,1,1,1]
        new_state, runs_scored = strike_out(current_state)

        self.assertEqual(new_state, [1,1,1,1])
        self.assertEqual(runs_scored, 0)
        