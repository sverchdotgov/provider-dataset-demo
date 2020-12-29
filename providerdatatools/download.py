#!/usr/bin/env python

import os
import sys
from shutil import copyfile
import paths, download_utils, extract_utils
import config as config_utils

for config_directory, config, metadata in config_utils.iterate_datasets():
    url = config_utils.render_url(config, metadata)
    download_directory = download_utils.build_download_directory(metadata)
    os.makedirs(download_directory, exist_ok=True)
    if "compression" in config:
        download_path = os.path.join(download_directory, "dataset.%s" % config["compression"])
        download_utils.download_with_progress(download_path, url)
        if config["compression"] != "zip":
            print("Unsupported compression: %s!" % config["compression"])
            sys.exit(1)
        extract_utils.unzip(download_path, download_directory)
    else:
        download_path = os.path.join(download_directory, "dataset.%s" % config["format"])
        download_utils.download_with_progress(download_path, url)
    src_config_file = config_utils.get_config_file(config_directory)
    dest_config_file = config_utils.get_config_file(download_directory)
    print("Copying config file from %s to %s" % (src_config_file, dest_config_file))
    copyfile(src_config_file, dest_config_file)
