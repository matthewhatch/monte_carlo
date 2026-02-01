import unittest
from monte_carlo.events import free_pass

class TestFreePass(unittest.TestCase):
    def test_free_pass_no_outs_empty(self):
        current_state = [0,0,0,0]
        new_state, runs_scored = free_pass(current_state)

        self.assertEqual(len(new_state), 4)
        self.assertEqual(new_state, [0,1,0,0])
        self.assertEqual(runs_scored, 0)

    def test_free_pass_no_outs_loaded(self):
        current_state = [0,1,1,1]
        new_state, runs_scored = free_pass(current_state)

        self.assertEqual(new_state, [0,1,1,1])
        self.assertEqual(runs_scored, 1)

    def test_free_pass_2_outs_loaded(self):
        current_state = [2,1,1,1]
        new_state, runs_scored = free_pass(current_state)

        self.assertEqual(new_state, [2,1,1,1])
        self.assertEqual(runs_scored, 1)

    def test_free_pass_1_out_runner_on_1_3(self):
        current_state = [1,1,0,1]
        new_state, runs_scored = free_pass(current_state)

        self.assertEqual(new_state, [1,1,1,1])
        self.assertEqual(runs_scored, 0)