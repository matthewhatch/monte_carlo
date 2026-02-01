"""Integration tests for Player class and game simulation"""

import unittest
from monte_carlo.classes.Player import Player
from monte_carlo.constants.players import TROUT16


# Remove 'name' key since Player doesn't accept it
TROUT16_FOR_PLAYER = {k: v for k, v in TROUT16.items() if k != 'name'}


class TestPlayerInit(unittest.TestCase):
    """Test Player initialization"""
    
    def setUp(self):
        """Set up test player"""
        self.player = Player(**TROUT16_FOR_PLAYER)
    
    def test_player_init(self):
        """Test that player initializes with correct stats"""
        self.assertEqual(self.player.plate_appearences, 681)
        self.assertEqual(self.player.at_bats, 554)
        self.assertEqual(self.player.strike_outs, 137)
        self.assertEqual(self.player.walks, 118)
    
    def test_player_individual_probabilities(self):
        """Test that player has probability attributes"""
        self.assertTrue(hasattr(self.player, 'p_error'))
        self.assertTrue(hasattr(self.player, 'p_walk'))
        self.assertTrue(hasattr(self.player, 'p_home_run'))
    
    def test_player_probabilities_range(self):
        """Test that all probabilities are in valid range"""
        probs = [self.player.p_error, self.player.p_walk, self.player.p_home_run,
                 self.player.p_single, self.player.p_double, self.player.p_triple]
        for prob in probs:
            self.assertGreaterEqual(prob, 0.0)
            self.assertLessEqual(prob, 1.0)


class TestPlayerSimulation(unittest.TestCase):
    """Test Player.simulate_ab() method"""
    
    def setUp(self):
        """Set up test player"""
        self.player = Player(**TROUT16_FOR_PLAYER)
    
    def test_simulate_ab_returns_tuple(self):
        """Test that simulate_ab returns (state, runs)"""
        state = [0, 0, 0, 0]
        result = self.player.simulate_ab(state)
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
    
    def test_simulate_ab_state_format(self):
        """Test that returned state has correct format"""
        state = [0, 0, 0, 0]
        new_state, runs = self.player.simulate_ab(state)
        self.assertEqual(len(new_state), 4)
        self.assertIsInstance(new_state[0], int)  # outs
        self.assertTrue(0 <= new_state[0] <= 3)
    
    def test_simulate_ab_runs_format(self):
        """Test that runs returned is non-negative integer"""
        state = [0, 0, 0, 0]
        new_state, runs = self.player.simulate_ab(state)
        self.assertIsInstance(runs, int)
        self.assertGreaterEqual(runs, 0)
    
    def test_simulate_ab_empty_bases(self):
        """Test simulate_ab with empty bases"""
        state = [0, 0, 0, 0]
        for _ in range(10):  # Run multiple times due to randomness
            new_state, runs = self.player.simulate_ab(state)
            self.assertIsNotNone(new_state)
    
    def test_simulate_ab_bases_loaded(self):
        """Test simulate_ab with bases loaded"""
        state = [0, 1, 1, 1]
        for _ in range(10):
            new_state, runs = self.player.simulate_ab(state)
            self.assertIsNotNone(new_state)


class TestPlayerRunsCreated(unittest.TestCase):
    """Test Player.runs_created() method"""
    
    def setUp(self):
        """Set up test player"""
        self.player = Player(**TROUT16_FOR_PLAYER)
    
    def test_runs_created_calculation(self):
        """Test that runs_created calculates correctly"""
        self.player.runs_created(10.5)
        self.assertGreater(self.player.runs_created, 0)
    
    def test_runs_created_with_zero(self):
        """Test runs_created with zero runs"""
        self.player.runs_created(0)
        self.assertGreaterEqual(self.player.runs_created, 0)
    
    def test_player_string_representation(self):
        """Test that player can be converted to string"""
        self.player.runs_created(7.55)
        player_str = str(self.player)
        self.assertIn('runs_created', player_str)


if __name__ == '__main__':
    unittest.main()
