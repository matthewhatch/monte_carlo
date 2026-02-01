import unittest
from monte_carlo.events import short_double

class TestShortDouble(unittest.TestCase):
    def test_short_double_no_outs_runner_on_2(self):
        current_state = [0,0,1,0]
        new_state, runs_scored = short_double(current_state)

        self.assertEqual(len(new_state), 4)
        self.assertEqual(new_state, [0,0,1,0])
        self.assertEqual(runs_scored, 1)

    def test_no_outs_runners_on_1_3(self):
        current_state = [0,1,0,1]
        new_state, runs_scored = short_double(current_state)

        self.assertEqual(len(new_state), 4)
        self.assertEqual(new_state, [0,0,1,1])
        self.assertEqual(runs_scored, 1)
    
    def test_no_outs_runners_on_1(self):
        current_state = [0,1,0,0]
        new_state, runs_scored = short_double(current_state)

        self.assertEqual(len(new_state), 4)
        self.assertEqual(new_state, [0,0,1,1])
        self.assertEqual(runs_scored, 0)
 