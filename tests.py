#!/usr/bin/env python3
"""
Unit Tests for keymonger
"""

import unittest
import logging
import keymonger.cli as keymonger
import argparse

LOG_FORMAT = "%(message)s"
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
LOG = logging.getLogger('test')

EXAMPLE_SOURCE_LIST = ["https://github.com/h4110w33n.keys"]
EXAMPLE_HASH_INPUT = "ssh-rsa AAAA...."
EXAMPLE_HASH = "ac169c6054b01f9bf6fa078eace5bdbf"
EXAMPLE_CONFIG_PATH = "examples/config-basic.json"
EXAMPLE_VERBOSITY = True

class FuncTests(unittest.TestCase):

	def test_key_grabber(self):
		LOG.debug("\n\tFunction: key_grabber()")
		LOG.debug("\tArgument(s): %s", str(EXAMPLE_SOURCE_LIST))
		results = keymonger.key_grabber(EXAMPLE_SOURCE_LIST)

		LOG.debug("\tTest 1: Return type == str")
		self.assertTrue(isinstance(results, str))
		LOG.debug("\tTest 1: PASS")

	def test_data_hasher(self):
		LOG.debug("\n\tFunction: data_hasher()")
		LOG.debug("\tArgument(s): %s", str(EXAMPLE_HASH_INPUT))
		results = keymonger.data_hasher(EXAMPLE_HASH_INPUT)

		LOG.debug("\tTest 1: Return type == str")
		self.assertTrue(isinstance(results, str))
		LOG.debug("\tTest 1: PASS")

		LOG.debug("\tTest 2: Returned hash == \"%s\"", EXAMPLE_HASH)
		self.assertEqual(results, EXAMPLE_HASH)
		LOG.debug("\tTest 2: PASS")


class UtilsTests(unittest.TestCase):

	# TODO: def test_update_permissions(self):
	# TODO: def test_write_authorized_keys(self):

	def test_load_config(self):
		LOG.debug("\n\tFunction: load_config()")
		LOG.debug("\tArgument(s): %s", str(EXAMPLE_CONFIG_PATH))
		results = keymonger.load_config(EXAMPLE_CONFIG_PATH)

		LOG.debug("\tTest 1: Return type == dict")
		self.assertTrue(isinstance(results, dict))
		LOG.debug("\tTest 1: PASS")

	def test_log_setup(self):
		LOG.debug("\n\tFunction: log_setup()")
		LOG.debug("\tArgument(s): verbosity = %s", EXAMPLE_VERBOSITY)
		results = keymonger.log_setup(EXAMPLE_VERBOSITY)

		LOG.debug("\tTest 1: Return type == logging.Logger")
		self.assertTrue(isinstance(results, logging.Logger))
		LOG.debug("\tTest 1: PASS")

	def test_arg_parser(self):
		LOG.debug("\n\tFunction: arg_parser()")
		LOG.debug("\tArgument(s): None")
		results = keymonger.arg_parser()

		LOG.debug("\tTest 1: Return type == argparse.Namespace")
		self.assertTrue(isinstance(results, argparse.Namespace))
		LOG.debug("\tTest 1: PASS")

class UtilsTests(unittest.TestCase):

	def test_main(self):
		LOG.debug("\n\tFunction: main()")
		LOG.debug("\tArgument(s): None")
		
		LOG.debug("\tTest 1: E2E Smoke test")
		results = keymonger.main()
		LOG.debug("\tTest 1: PASS")

if __name__ == '__main__':
    unittest.main(verbosity=2)
