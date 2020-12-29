#!/usr/bin/env python

import zipfile

def unzip(file_name, dest_dir):
    print("Unzipping %s to %s" % (file_name, dest_dir))
    with zipfile.ZipFile(file_name, 'r') as zip_ref:
        zip_ref.extractall(dest_dir)
