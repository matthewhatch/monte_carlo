import unittest
from monte_carlo.events import single, short_single

class TestBaseballFunctions(unittest.TestCase):
    
    def test_single(self):
        current_state = [0, 0, 1, 0]  # Example current state
        new_state, runs_scored = single(current_state)
        # Add assertions to check if the function behaves as expected
        self.assertEqual(len(new_state), 4)
        self.assertTrue(0 <= runs_scored <= 1)  # Ensure runs scored is within expected range
    
    # Add similar test methods for other functions like double, triple, home_run, etc.
    def test_short_single_no_outs_empty(self):
        current_state = [0,0,0,0]
        new_state, runs_scored = short_single(current_state)
        self.assertEqual(len(new_state), 4)
        self.assertEqual(new_state[0], 0)
        self.assertEqual(new_state[1], 1)
        self.assertEqual(new_state[2], 0)
        self.assertEqual(new_state[3], 0)
        self.assertEqual(runs_scored, 0)
    
    def test_short_single_no_outs_runner_first(self):
        current_state = [0,1,0,0]
        new_state, runs_scored = short_single(current_state)
        self.assertEqual(len(new_state), 4)
        self.assertEqual(new_state[0], 0)
        self.assertEqual(new_state[1], 1)
        self.assertEqual(new_state[2], 1)
        self.assertEqual(new_state[3], 0)
        self.assertEqual(runs_scored, 0)
   
    def test_short_single_no_outs_runner_on_1_2(self):
        current_state = [0,1,1,0]
        new_state, runs_scored = short_single(current_state)
        self.assertEqual(len(new_state), 4)
        self.assertEqual(new_state[0], 0)
        self.assertEqual(new_state[1], 1)
        self.assertEqual(new_state[2], 1)
        self.assertEqual(new_state[3], 1)
        self.assertEqual(runs_scored, 0)

    def test_short_single_no_outs_runner_on_1_2_3(self):
        current_state = [0,1,1,1]
        new_state, runs_scored = short_single(current_state)
        self.assertEqual(len(new_state), 4)
        self.assertEqual(new_state[0], 0)
        self.assertEqual(new_state[1], 1)
        self.assertEqual(new_state[2], 1)
        self.assertEqual(new_state[3], 1)
        self.assertEqual(runs_scored, 1)

    def test_short_single_2_outs_runner_on_1_2_3(self):
        current_state = [2,1,1,1]
        new_state, runs_scored = short_single(current_state)
        self.assertEqual(len(new_state), 4)
        self.assertEqual(new_state[0], 2)
        self.assertEqual(new_state[1], 1)
        self.assertEqual(new_state[2], 1)
        self.assertEqual(new_state[3], 1)
        self.assertEqual(runs_scored, 1)

    def test_short_single_2_outs_runner_on_1_3(self):
        current_state = [2,1,0,1]
        new_state, runs_scored = short_single(current_state)
        self.assertEqual(len(new_state), 4)
        self.assertEqual(new_state[0], 2)
        self.assertEqual(new_state[1], 1)
        self.assertEqual(new_state[2], 1)
        self.assertEqual(new_state[3], 0)
        self.assertEqual(runs_scored, 1)


if __name__ == '__main__':
    unittest.main()
