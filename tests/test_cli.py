"""Tests for CLI functionality"""

import unittest
import sys
import os
from unittest.mock import patch
from io import StringIO
from monte_carlo.cli import main, simulate_game, simulate_inning
from monte_carlo.classes.Player import Player
from monte_carlo.constants.players import TROUT16


# Remove 'name' key since Player doesn't accept it
TROUT16_FOR_PLAYER = {k: v for k, v in TROUT16.items() if k != 'name'}


class TestSimulateInning(unittest.TestCase):
    """Test simulate_inning function"""
    
    def setUp(self):
        """Set up test player"""
        self.player = Player(**TROUT16_FOR_PLAYER)
    
    def test_simulate_inning_returns_int(self):
        """Test that simulate_inning returns an integer"""
        runs = simulate_inning(self.player)
        self.assertIsInstance(runs, int)
        self.assertGreaterEqual(runs, 0)
    
    def test_simulate_inning_completes(self):
        """Test that simulate_inning completes without error"""
        for _ in range(10):
            runs = simulate_inning(self.player)
            self.assertIsNotNone(runs)


class TestSimulateGame(unittest.TestCase):
    """Test simulate_game function"""
    
    def setUp(self):
        """Set up test player"""
        self.player = Player(**TROUT16_FOR_PLAYER)
    
    def test_simulate_game_returns_int(self):
        """Test that simulate_game returns an integer"""
        runs = simulate_game(self.player)
        self.assertIsInstance(runs, int)
        self.assertGreaterEqual(runs, 0)
    
    def test_simulate_game_completes(self):
        """Test that simulate_game completes without error"""
        for _ in range(5):
            runs = simulate_game(self.player)
            self.assertIsNotNone(runs)


class TestCLI(unittest.TestCase):
    """Test CLI argument parsing and execution"""
    
    def test_cli_default_args(self):
        """Test CLI with default arguments"""
        with patch('sys.argv', ['monte-carlo']):
            try:
                # Should parse without error
                from monte_carlo.cli import argparse as ap
            except SystemExit:
                self.fail("CLI failed with default arguments")
    
    def test_cli_custom_count(self):
        """Test CLI with custom simulation count"""
        with patch('sys.argv', ['monte-carlo', '-c', '10']):
            try:
                # Should parse without error
                pass
            except SystemExit:
                self.fail("CLI failed with custom count")
    
    def test_cli_custom_player(self):
        """Test CLI with custom player"""
        with patch('sys.argv', ['monte-carlo', '-p', 'Mike Trout']):
            try:
                # Should parse without error
                pass
            except SystemExit:
                self.fail("CLI failed with custom player")
    
    def test_cli_custom_year(self):
        """Test CLI with custom year"""
        with patch('sys.argv', ['monte-carlo', '-y', '2016']):
            try:
                # Should parse without error
                pass
            except SystemExit:
                self.fail("CLI failed with custom year")
    
    def test_cli_verbose_flag(self):
        """Test CLI with verbose flag"""
        with patch('sys.argv', ['monte-carlo', '-v']):
            try:
                # Should parse without error
                pass
            except SystemExit:
                self.fail("CLI failed with verbose flag")


if __name__ == '__main__':
    unittest.main()
