import unittest
from events import long_double

class TestLongDouble(unittest.TestCase):
    def test_long_double_no_outs_empty(self):
        current_state = [0,0,0,0]
        new_state, runs_scored = long_double(current_state)

        self.assertEqual(len(new_state), 4)
        self.assertEqual(new_state, [0,0,1,0])
        self.assertEqual(runs_scored, 0)

    def test_long_double_no_outs_1_and_3(self):
        current_state = [0,1,0,1]
        new_state, runs_scored = long_double(current_state)

        self.assertEqual(new_state, [0,0,1,0])
        self.assertEqual(runs_scored, 2)

    def test_long_double_no_outs_bases_loaded(self):
        current_state = [0,1,1,1]
        new_state, runs_scored = long_double(current_state)

        self.assertEqual(new_state, [0,0,1,0])
        self.assertEqual(runs_scored, 3)
    
    def test_long_double_1_out_1(self):
        current_state = [1,1,0,0]
        new_state, runs_scored = long_double(current_state)

        self.assertEqual(new_state, [1,0,1,0])
        self.assertEqual(runs_scored, 1)

