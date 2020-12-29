#!/usr/bin/env python

import os
import yaml
import sys
from shutil import copyfile
import paths, download_utils, extract_utils
import config as config_utils

config_root = paths.get_dataset_configuration_root()
for organization_type in os.listdir(config_root):
    organization_path = os.path.join(config_root, organization_type)
    for provider_subset in os.listdir(organization_path):
        provider_subset_path = os.path.join(organization_path, provider_subset)
        for datastore in os.listdir(provider_subset_path):
            datastore_path = os.path.join(provider_subset_path, datastore)
            for dataset in os.listdir(datastore_path):
                dataset_path = os.path.join(datastore_path, dataset)
                config_file = os.path.join(dataset_path, "config.yaml")
                with open(config_file) as f:
                    config = yaml.load(f, Loader=yaml.FullLoader)
                metadata = config_utils.build_metadata(organization_type, provider_subset, datastore, dataset)
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
                copyfile(config_file, os.path.join(download_directory, "config.yaml"))
