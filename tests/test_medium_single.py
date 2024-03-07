import unittest
from events import medium_single

class TestMediumSingle(unittest.TestCase):
    def test_medium_no_outs_empty(self):
        current_state = [0,0,0,0]
        new_state, runs_scored = medium_single(current_state)

        self.assertEqual(len(new_state), 4)
        self.assertEqual(new_state[0],0)
        self.assertEqual(new_state[1],1)
        self.assertEqual(new_state[2],0)
        self.assertEqual(new_state[3],0)
        self.assertEqual(runs_scored,0)

    def test_medium_no_outs_runners_on_1(self):
        current_state = [0,1,0,0]
        new_state, runs_scored = medium_single(current_state)

        self.assertEqual(len(new_state), 4)
        self.assertEqual(new_state[0],0)
        self.assertEqual(new_state[1],1)
        self.assertEqual(new_state[2],1)
        self.assertEqual(new_state[3],0)
        self.assertEqual(runs_scored,0)

    
    def test_medium_no_outs_runners_on_2(self):
        current_state = [0,0,1,0]
        new_state, runs_scored = medium_single(current_state)

        self.assertEqual(len(new_state), 4)
        self.assertEqual(new_state[0],0)
        self.assertEqual(new_state[1],1)
        self.assertEqual(new_state[2],0)
        self.assertEqual(new_state[3],0)
        self.assertEqual(runs_scored,1)
