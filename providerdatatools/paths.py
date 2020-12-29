#!/usr/bin/env python

import os
import git

def get_git_root(path):
    git_repo = git.Repo(path, search_parent_directories=True)
    git_root = git_repo.working_dir
    return(git_root)

def get_dataset_configuration_root():
    return os.path.join(
        get_git_root(os.path.dirname(os.path.realpath(__file__))),
        "dataset-configuration")
