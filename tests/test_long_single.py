import unittest
from monte_carlo.events import long_single

class TestLongSingle(unittest.TestCase):
    def test_long_no_outs_empty(self):
        current_state = [0,0,0,0]
        new_state, runs_scored = long_single(current_state)

        self.assertEqual(len(new_state), 4)
        self.assertEqual(new_state,[0,1,0,0])
        self.assertEqual(runs_scored,0)

    def test_long_no_outs_runners_on_1(self):
        current_state = [0,1,0,0]
        new_state, runs_scored = long_single(current_state)

        self.assertEqual(len(new_state), 4)
        self.assertEqual(new_state, [0,1,0,1])
        self.assertEqual(runs_scored,0)

    
    def test_long_no_outs_runners_on_2(self):
        current_state = [0,0,1,0]
        new_state, runs_scored = long_single(current_state)

        self.assertEqual(len(new_state), 4)
        self.assertEqual(new_state, [0,1,0,0])
        self.assertEqual(runs_scored,1)

    def test_long_no_outs_runners_on_3(self):
        current_state = [0,0,0,1]
        new_state, runs_scored = long_single(current_state)

        self.assertEqual(len(new_state), 4)
        self.assertEqual(new_state, [0,1,0,0])
        self.assertEqual(runs_scored,1)

    def test_long_no_outs_runners_on_1_3(self):
        current_state = [0,1,0,1]
        new_state, runs_scored = long_single(current_state)

        self.assertEqual(len(new_state), 4)
        self.assertEqual(new_state, [0,1,0,1])
        self.assertEqual(runs_scored,1)

    def test_long_1_outs_runners_on_1_3(self):
        current_state = [1,1,0,1]
        new_state, runs_scored = long_single(current_state)

        self.assertEqual(len(new_state), 4)
        self.assertEqual(new_state, [1,1,0,1])
        self.assertEqual(runs_scored,1)
