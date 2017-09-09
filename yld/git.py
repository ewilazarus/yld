"""
yld.git
~~~~~~~

This module contains the interface for communicating with Git
"""
import sys
import subprocess


def _call(command):
    try:
        return subprocess.check_output(command.split(' '),
                                       universal_newlines=True)
    except subprocess.CalledProcessError:
        sys.exit(1)


def _fetch_tags():
    _call('git fetch --tags')


def exists():
    """
    Returns True if there's a valid git installation, otherwise False
    """
    try:
        _call('git --version')
        return True
    except:
        return False

def is_committed():
    """
    Returns True if repository is committed, otherwise False
    """
    return 'nothing to commit' in _call('git status')


def list_tags():
    """
    Returns a list of tags
    """
    _fetch_tags()
    return [t for t in _call('git tag').strip().split('\n') if t != '']


def create_tag(tag):
    """
    Creates a tag
    """
    _call('git tag ' + str(tag))


def delete_tag(tag):
    """
    Deletes a tag
    """
    _call('git tag -d ' + str(tag))


def push_tag(tag):
    """
    Pushes a tag into the upstream
    """
    _call('git push origin ' + str(tag))

