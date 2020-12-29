#!/usr/bin/env python

from datetime import datetime
from jinja2 import Template
import os
import yaml
import paths

# TODO: Actually make this a config object that can return this URL and metadata. Even better, just
# use an existing "yaml config" python library and override these fields.
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

def get_config_file(config_directory):
    return os.path.join(config_directory, "config.yaml")

def iterate_datasets():
    config_root = paths.get_dataset_configuration_root()
    for organization_type in os.listdir(config_root):
        organization_path = os.path.join(config_root, organization_type)
        for provider_subset in os.listdir(organization_path):
            provider_subset_path = os.path.join(organization_path, provider_subset)
            for datastore in os.listdir(provider_subset_path):
                datastore_path = os.path.join(provider_subset_path, datastore)
                for dataset in os.listdir(datastore_path):
                    dataset_path = os.path.join(datastore_path, dataset)
                    config_file = get_config_file(dataset_path)
                    with open(config_file) as f:
                        config = yaml.load(f, Loader=yaml.FullLoader)
                    metadata = build_metadata(organization_type, provider_subset, datastore, dataset)
                    yield dataset_path, config, metadata

def iterate_download_configs():
    config_root = paths.get_download_root()
    for organization_type in os.listdir(config_root):
        if organization_type == "README.md":
            continue
        organization_path = os.path.join(config_root, organization_type)
        for provider_subset in os.listdir(organization_path):
            provider_subset_path = os.path.join(organization_path, provider_subset)
            for datastore in os.listdir(provider_subset_path):
                datastore_path = os.path.join(provider_subset_path, datastore)
                for dataset in os.listdir(datastore_path):
                    dataset_path = os.path.join(datastore_path, dataset)
                    latest = max([datetime.fromisoformat(timestamp) for timestamp in os.listdir(dataset_path)])
                    latest_path = os.path.join(dataset_path, str(latest.isoformat()))
                    config_file = get_config_file(latest_path)
                    with open(config_file) as f:
                        config = yaml.load(f, Loader=yaml.FullLoader)
                    metadata = build_metadata(organization_type, provider_subset, datastore, dataset)
                    yield dataset_path, config, metadata
