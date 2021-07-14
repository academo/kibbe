#!/usr/bin/env python3
import configparser
import subprocess
import sys

config_file_path = './setup.cfg'
git_version = str(sys.argv[1])

if len(git_version) == 0:
    exit(1)

git_version = git_version[1:]

config = configparser.ConfigParser()
config.read(config_file_path)
current = config['metadata']['version']
if current != git_version:
    config.set('metadata', 'version', git_version)

with open(config_file_path, 'w') as configfile:
    config.write(configfile)
