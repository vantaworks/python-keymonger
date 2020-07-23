#!/usr/bin/env python3
""" Setup for Keymonger """
from setuptools import setup
from keymonger.getter import __version__

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
	name='Keymonger',
	version=__version__,
	author="Robert Rice",
	author_email="h4110w33n@gmail.com",
	url='https://github.com/h4110w33n',
	description='A key management utility.',
	long_description='A key management utility.',
	keywords=['keys'],
	classifiers=[
		'Environment :: Console'
	],
	requires=required,
	install_requires=required,
	provides=['keymonger'],
	entry_points={
		'console_scripts': ['keymonger=keymonger:main'],
	},
	platforms='linux',
	license='GNU General Public License v3 (GPLv3)',
	packages=['keymonger'],
)