#!/usr/bin/env python3
from pathlib import PurePath
import configparser
import subprocess

config_file_path = './setup.cfg'
git_version = subprocess.getoutput('git describe --tags --abbrev=0')[1:]

config = configparser.ConfigParser()
config.read(config_file_path)
current = config['metadata']['version']
if current != git_version:
    config.set('metadata', 'version', git_version)

with open(config_file_path, 'w') as configfile:
    config.write(configfile)
