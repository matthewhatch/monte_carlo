#!/usr/bin/env python3
"""Generate CSV files from player constants for testing"""

import os
from utils.players import create_csv_from_constant
from constants.players import TROUT16

# Create data directory if it doesn't exist
os.makedirs('data', exist_ok=True)

# Generate CSV files from constants
create_csv_from_constant('mike trout', '2016', TROUT16)

print('Test data setup complete!')
