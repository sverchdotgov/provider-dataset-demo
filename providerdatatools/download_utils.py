#!/usr/bin/env python

import os
import requests
import sys
import paths

def build_download_directory(metadata):
    return os.path.join(
        paths.get_git_root(os.path.dirname(os.path.realpath(__file__))),
        "data",
        metadata["organization_type"],
        metadata["provider_subset"],
        metadata["datastore"],
        metadata["dataset"],
        metadata["datetime"])

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
