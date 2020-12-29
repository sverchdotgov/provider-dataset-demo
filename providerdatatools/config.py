#!/usr/bin/env python

from datetime import datetime
from jinja2 import Template

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
