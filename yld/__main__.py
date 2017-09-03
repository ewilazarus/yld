#!/usr/bin/python
"""
yld
~~~

This module contains the source code for `yld`

`yld` is an utility tool created to ease tag triggered deployments.
"""
import sys
import click
from . import git
from .version import VersionCatalog


def get_target_version(latest, mode, label):
    if mode is None:
        return latest.bump('revision', label)
    else:
        return latest.bump(mode) \
                if label is None \
                else latest.bump(mode).root.bump('revision', label)

def bump(versions, mode, label):
    target_version = get_target_version(versions.latest(label), mode, label)

    click.echo()

    if click.confirm('Do you want to create the tag {tag}?'.format(
        tag=click.style(str(target_version), fg='yellow')),
        default=True, abort=True):
        git.create_tag(target_version)

    if click.confirm('Do you want to push the tag {tag} into the upstream?'.format(
        tag=click.style(str(target_version), fg='yellow')),
        default=True):
        git.push_tag(target_version)
        click.echo('Done!')
    else:
        git.delete_tag(target_version)
        click.echo('Aborted!')

def print_latest_stable(versions):
    ls = str(versions._latest_stable())
    ls = 'N/A' if ls == 'v0.1.0' and versions.stable_count() == 0 else ls

    click.echo('=> Latest stable: {version}'.format(
        version=click.style(ls, fg='yellow' if ls != 'N/A' else 'magenta')
    ))

def print_latest_revision(versions, label):
    lr = str(versions._latest_revision(label))
    lr = lr if '-' in lr else 'N/A'

    click.echo('=> Latest relative revision ({label}): {version}'.format(
        label=click.style(label, fg='blue'),
        version=click.style(lr, fg='yellow' if lr != 'N/A' else 'magenta')
    ))

@click.command(name='yld')
@click.option('-M', '--major', 'mode', flag_value='major')
@click.option('-m', '--minor', 'mode', flag_value='minor')
@click.option('-p', '--patch', 'mode', flag_value='patch')
@click.option('-l', '--label', default=None, type=str)
def main(mode, label):
    """
    Tag triggered deployment helper
    """
    if not git.exists():
        click.secho('You must have git installed to use yld.', fg='red')
        sys.exit(1)

    if not git.is_committed():
        click.secho('You must commit or stash your work before proceeding.',
                    fg='red')
        sys.exit(1)

    if not git.is_pushed():
        click.secho('You must push your commits into the upstream before proceeding.',
                    fg='red')
        sys.exit(1)

    if mode is None and label is None:
        click.secho('You must specify either a mode or a label.', fg='red')
        sys.exit(1)

    click.secho('Fetching tags from the upstream ...')
    versions = VersionCatalog.parse(git.list_tags())

    print_latest_stable(versions)
    if label is not None:
        print_latest_revision(versions, label)

    bump(versions, mode, label)


if __name__ == '__main__':
    main()
