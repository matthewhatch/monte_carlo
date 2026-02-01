import unittest
from monte_carlo.events import ground_out

class TestGroundOut(unittest.TestCase):
    def test_ground_out_no_outs_empty(self):
        current_state = [0,0,0,0]
        new_state, runs_scored = ground_out(current_state)

        self.assertEqual(new_state, [1,0,0,0])
        self.assertEqual(runs_scored, 0)
    
    def test_ground_out_no_outs_runners_on_first(self):
        current_state = [0,1,0,0]
        new_state, runs_scored = ground_out(current_state)

        self.assertEqual(new_state, [1,1,0,0])
        self.assertEqual(runs_scored, 0)

    def test_ground_out_no_outs_runners_on_1_2(self):
        current_state = [0,1,1,0]
        new_state, runs_scored = ground_out(current_state)

        self.assertEqual(new_state, [1,1,1,0])
        self.assertEqual(runs_scored, 0)

    def test_ground_out_no_outs_bases_loaded(self):
        current_state = [0,1,1,1]
        new_state, runs_scored = ground_out(current_state)

        self.assertEqual(new_state, [1,1,1,1])
        self.assertEqual(runs_scored, 0)

    def test_ground_out_2_outs_bases_loaded(self):
        current_state = [2,1,1,1]
        new_state, runs_scored = ground_out(current_state)

        self.assertEqual(new_state[0], 3)
        self.assertEqual(runs_scored, 0)

    def test_ground_out_1_out_runner_on_3(self):
        current_state = [1,0,0,1]
        new_state, runs_scored = ground_out(current_state)

        self.assertEqual(new_state, [2,0,0,0])
        self.assertEqual(runs_scored, 1)