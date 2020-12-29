#!/usr/bin/env python

import git
import os
import yaml
from jinja2 import Template
from datetime import datetime
import zipfile
import requests
import sys
from shutil import copyfile

def get_git_root(path):
    git_repo = git.Repo(path, search_parent_directories=True)
    git_root = git_repo.working_dir
    return(git_root)

def get_dataset_configuration_root():
    return os.path.join(
        get_git_root(os.path.dirname(os.path.realpath(__file__))),
        "dataset-configuration")

def build_metadata(organization_type, provider_subset, datastore, dataset):
    today = datetime.today()
    return {
        "organization_type": organization_type,
        "provider_subset": provider_subset,
        "datastore": datastore,
        "dataset": dataset,
        "month_name": today.strftime("%B"),
        "month": today.month,
        "year": today.year,
        "datetime": str(today.isoformat())
        }

def render_url(config, metadata):
    template = Template(config['url'])
    return template.render(metadata)

def download_with_progress(file_name, link):
    with open(file_name, "wb") as f:
        print ("Downloading %s and saving as %s" % (link, file_name))
        response = requests.get(link, stream=True)
        total_length = response.headers.get('content-length')

        if total_length is None: # no content length header
            print("No content length header, cannot display progress bar")
            dl = 0
            for data in response.iter_content(chunk_size=4096):
                dl += len(data)
                f.write(data)
                sys.stdout.write("\r%.1fMB" % (dl/1024/1024))
                sys.stdout.flush()
        else:
            dl = 0
            total_length = int(total_length)
            for data in response.iter_content(chunk_size=4096):
                dl += len(data)
                f.write(data)
                done = int(50 * dl / total_length)
                sys.stdout.write("\r[%s%s] %.1fMB/%.1fMB" % ('=' * done, ' ' * (50-done), dl/1024/1024, total_length/1024/1024) )
                sys.stdout.flush()
        print ("Download of %s complete." % (file_name))

def unzip(file_name, dest_dir):
    print("Unzipping %s to %s" % (file_name, dest_dir))
    with zipfile.ZipFile(file_name, 'r') as zip_ref:
        zip_ref.extractall(dest_dir)

def build_download_directory(metadata):
    return os.path.join(
        get_git_root(os.path.dirname(os.path.realpath(__file__))),
        "data",
        metadata["organization_type"],
        metadata["provider_subset"],
        metadata["datastore"],
        metadata["dataset"],
        metadata["datetime"])

config_root = get_dataset_configuration_root()
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
                metadata = build_metadata(organization_type, provider_subset, datastore, dataset)
                url = render_url(config, metadata)
                download_directory = build_download_directory(metadata)
                os.makedirs(download_directory, exist_ok=True)
                if "compression" in config:
                    download_path = os.path.join(download_directory, "dataset.%s" % config["compression"])
                    download_with_progress(download_path, url)
                    if config["compression"] != "zip":
                        print("Unsupported compression: %s!" % config["compression"])
                        sys.exit(1)
                    unzip(download_path, download_directory)
                else:
                    download_path = os.path.join(download_directory, "dataset.%s" % config["format"])
                    download_with_progress(download_path, url)
                copyfile(config_file, os.path.join(download_directory, "config.yaml"))
