#!/usr/bin/env python

import os
import sys
from shutil import copyfile
import paths, download_utils, extract_utils
import config as config_utils

for config_directory, config, metadata in config_utils.iterate_download_configs():
    print(config_directory, config, metadata)
