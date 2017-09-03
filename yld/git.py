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
    try:
        _call('git --version')
        return True
    except:
        return False


def list_tags():
    _fetch_tags()
    return [t for t in _call('git tag').strip().split('\n') if t != '']


def create_tag(tag):
    _call('git tag ' + str(tag))


def delete_tag(tag):
    _call('git tag -d ' + str(tag))


def push_tag(tag):
    _call('git push origin ' + str(tag))


def is_committed():
    return 'nothing to commit' in _call('git status')


def is_pushed():
    return 'Your branch is up-to-date with' in _call('git status')

