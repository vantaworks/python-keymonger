#!/usr/bin/env python3
"""
Unit Tests for keymonger
"""

import unittest
import logging
import keymonger
import argparse
import os
import configparser
from pathlib import Path

LOG_FORMAT = "%(message)s"
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
LOG = logging.getLogger('test')

TEST_USER = os.getlogin()
TEST_CONFIG_FILE = "tests/keymonger-{}.conf".format(TEST_USER)
TEST_URL1 = ["https://github.com/h4110w33n.keys"]
TEST_URL2 = "https://github.com/h4110w33n.keys"
TEST_URL3 = "https://github.com/h4110w33n.keys,https://github.com/h4110w33n.keys"
TEST_DESTINATION1 = "tests/authorized_keys_{}".format(TEST_USER)
TEST_DESTINATION2 = "tests/fake_keys"

class KeymongerTests(unittest.TestCase):

	def test_load_configs(self):
		LOG.debug("")
		LOG.debug("\n\tFunction: load_configs()")
        LOG.debug("\tArgument(s): config_path = %s", TEST_CONFIG_FILE)
		results = keymonger.load_configs(TEST_CONFIG_FILE)
		
		LOG.debug("\tTest 1: Return types == configparser.ConfigParser")
		for result in results:
			self.assertTrue(isinstance(result, configparser.ConfigParser))
		LOG.debug("\tTest 1: PASS")

		[global_config, user_config] = results
		
		LOG.debug("\tTest 2: Verify options have been read for Global Config")
		options = ["set_permissions", "verbose_logging", "idempotency_check", "include_config"]
		for i,option in enumerate(options):
			LOG.debug("\t\t2.%s - Verifying option %s", i, option)
			self.assertTrue(option in global_config["global"])
		LOG.debug("\tTest 2: PASS")

		LOG.debug("\tTest 3: Verify options have been read for User Config")
		options = ["key_sources", "key_destination"]
		for i,user in enumerate(user_config.sections()):
			LOG.debug("\t\t3.%s - Checking user %s", i, user)
			for j,option in enumerate(options):
				LOG.debug("\t\t3.%s.%s - Verifying option %s", i, j, option)
				self.assertTrue(option in user_config[user])
		LOG.debug("\tTest 3: PASS")

	def test_get_remote_keys(self):
		LOG.debug("")

		results = keymonger.get_remote_keys(TEST_URL1)
		LOG.debug("\tTest 1: Return types == str from non-list")
		self.assertTrue(isinstance(results, str))
		LOG.debug("\tTest 1: PASS")

		results = keymonger.get_remote_keys(TEST_URL2)
		LOG.debug("\tTest 2: Return types == str from str only")
		self.assertTrue(isinstance(results, str))
		LOG.debug("\tTest 2: PASS")

		results = keymonger.get_remote_keys(TEST_URL3)
		LOG.debug("\tTest 3: Return types == str from list")
		self.assertTrue(isinstance(results, str))
		LOG.debug("\tTest 3: PASS")

	def test_log_setup(self):
		LOG.debug("")

		logger = keymonger.log_setup(False)
		LOG.debug("\tTest 1: Return types == logging.Logger Non-verbose")
		self.assertTrue(isinstance(logger, logging.Logger))
		LOG.debug("\tTest 1: PASS")

		logger = keymonger.log_setup(True)
		LOG.debug("\tTest 2: Return types == logging.Logger Verbose")
		self.assertTrue(isinstance(logger, logging.Logger))
		LOG.debug("\tTest 2: PASS")

	def test_arg_parser(self):
		LOG.debug("")

		results = keymonger.arg_parser()
		LOG.debug("\tTest 1: Return types == argparse.Namespace")
		self.assertTrue(isinstance(results, argparse.Namespace))
		LOG.debug("\tTest 1: PASS")

	def test_set_key_destination(self):
		LOG.debug("")

		results = keymonger.set_key_destination(TEST_USER)
		LOG.debug("\tTest 1: Return types == str")
		self.assertTrue(isinstance(results, str))
		LOG.debug("\tTest 1: PASS")

	def test_read_key_destination(self):
		LOG.debug("")

		results = keymonger.read_key_destination(TEST_DESTINATION1)
		LOG.debug("\tTest 1: Return types == str for existing keys")
		self.assertTrue(isinstance(results, str))
		LOG.debug("\tTest 1: PASS")

		results = keymonger.read_key_destination(TEST_DESTINATION2)
		LOG.debug("\tTest 2: Return types == str for non-existant keys")
		self.assertTrue(isinstance(results, str))
		LOG.debug("\tTest 2: PASS")

	def test_write_authorized_keys(self):
		LOG.debug("")

		keymonger.write_authorized_keys(TEST_DESTINATION2, "asdf")
		results = Path(TEST_DESTINATION2).is_file()
		LOG.debug("\tTest 1: File is created")
		self.assertTrue(results)
		LOG.debug("\tTest 1: PASS")

		keymonger.update_permissions(TEST_USER, TEST_DESTINATION2)
		results = Path(TEST_DESTINATION2).owner()
		LOG.debug("\tTest 2: File owned by correct user")
		self.assertTrue(results == TEST_USER)
		LOG.debug("\tTest 2: PASS")

		# print({section: dict(global_config[section]) for section in global_config.sections()})
	# def test_print(self, config):
	# 	print("Just a doc")
	# 	print({section: dict(config[section]) for section in config.sections()})

if __name__ == '__main__':
    unittest.main(verbosity=2)
