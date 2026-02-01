import unittest
from monte_carlo.events import error

class TestError(unittest.TestCase):
    def test_error_no_outs_empty(self):
        current_state = [0,0,0,0]
        new_state, runs_scored = error(current_state)

        self.assertEqual(len(new_state), 4)
        self.assertEqual(new_state, [0,1,0,0])
        self.assertEqual(runs_scored, 0)
    
    def test_error_1_out_bases_loaded(self):
        current_state = [1,1,1,1]
        new_state, runs_scored = error(current_state)

        self.assertEqual(len(new_state), 4)
        self.assertEqual(new_state, [1,1,1,1])
        self.assertEqual(runs_scored, 1)
    