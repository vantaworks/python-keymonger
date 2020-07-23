#!/usr/bin/env python3
"""
Unit Tests for keymonger
"""

import unittest
import logging
import keymonger
import argparse

LOG_FORMAT = "%(message)s"
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
LOG = logging.getLogger('test')

# This is a placeholder for the time being

if __name__ == '__main__':
    unittest.main(verbosity=2)
