"""Tests for player data utilities"""

import unittest
import os
import tempfile
import shutil
import pandas as pd
from monte_carlo.utils.players import (
    get_stats,
    _get_from_csv,
    create_csv_from_constant,
    name_search
)
from monte_carlo.constants.players import TROUT16


class TestCreateCSVFromConstant(unittest.TestCase):
    """Test CSV generation from player constants"""
    
    def setUp(self):
        """Create temporary directory for test CSV files"""
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
        os.makedirs('data', exist_ok=True)
    
    def tearDown(self):
        """Clean up temporary directory"""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)
    
    def test_create_csv_from_constant_creates_file(self):
        """Test that create_csv_from_constant creates a file"""
        create_csv_from_constant('mike trout', '2016', TROUT16)
        self.assertTrue(os.path.exists('data/players_2016.csv'))
    
    def test_csv_has_correct_columns(self):
        """Test that created CSV has expected columns"""
        create_csv_from_constant('mike trout', '2016', TROUT16)
        df = pd.read_csv('data/players_2016.csv')
        self.assertIn('name', df.columns)
        self.assertIn('plate_appearences', df.columns)
        self.assertIn('home_runs', df.columns)
    
    def test_csv_has_correct_data(self):
        """Test that CSV contains correct player data"""
        create_csv_from_constant('mike trout', '2016', TROUT16)
        df = pd.read_csv('data/players_2016.csv')
        self.assertEqual(df.iloc[0]['name'], 'mike trout')
        self.assertEqual(df.iloc[0]['home_runs'], 29)
        self.assertEqual(df.iloc[0]['plate_appearences'], 681)


class TestGetFromCSV(unittest.TestCase):
    """Test CSV reading functionality"""
    
    def setUp(self):
        """Create temporary directory with test CSV"""
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
        os.makedirs('data', exist_ok=True)
        
        # Create test CSV
        create_csv_from_constant('mike trout', '2016', TROUT16)
    
    def tearDown(self):
        """Clean up temporary directory"""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)
    
    def test_get_from_csv_returns_dict(self):
        """Test that _get_from_csv returns a dictionary"""
        stats = _get_from_csv('mike trout', '2016')
        self.assertIsInstance(stats, dict)
    
    def test_get_from_csv_contains_expected_keys(self):
        """Test that returned dict has expected keys"""
        stats = _get_from_csv('mike trout', '2016')
        self.assertIn('plate_appearences', stats)
        self.assertIn('home_runs', stats)
        self.assertIn('strike_outs', stats)
    
    def test_get_from_csv_nonexistent_file(self):
        """Test _get_from_csv with nonexistent year"""
        stats = _get_from_csv('mike trout', '2099')
        self.assertIsNone(stats)
    
    def test_get_from_csv_nonexistent_player(self):
        """Test _get_from_csv with nonexistent player"""
        stats = _get_from_csv('john doe', '2016')
        self.assertIsNone(stats)


class TestGetStats(unittest.TestCase):
    """Test get_stats function"""
    
    def setUp(self):
        """Create temporary directory with test CSV"""
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
        os.makedirs('data', exist_ok=True)
        
        # Create test CSV
        create_csv_from_constant('mike trout', '2016', TROUT16)
        
        # Set CI environment to skip web scraping
        os.environ['CI'] = 'true'
    
    def tearDown(self):
        """Clean up temporary directory"""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)
        if 'CI' in os.environ:
            del os.environ['CI']
    
    def test_get_stats_returns_dict(self):
        """Test that get_stats returns a dictionary"""
        stats = get_stats('mike trout', '2016')
        self.assertIsInstance(stats, dict)
    
    def test_get_stats_cached_data(self):
        """Test that get_stats retrieves cached CSV data"""
        stats = get_stats('mike trout', '2016')
        self.assertEqual(stats['home_runs'], 29)
        self.assertEqual(stats['plate_appearences'], 681)
    
    def test_get_stats_missing_cached_data_raises_error(self):
        """Test that get_stats raises error for missing data in CI"""
        with self.assertRaises(Exception):
            get_stats('babe ruth', '2016')


if __name__ == '__main__':
    unittest.main()
