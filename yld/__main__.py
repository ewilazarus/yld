#!/usr/bin/python
"""
yld
~~~

This module contains the source code for `yld`

`yld` is an utility tool created to ease semver tag triggered deployments.
"""
import os
import sys
import click
from . import git
from .tag import TagHandler


@click.command(name='yld')
@click.option('-M', '--major', 'target', flag_value='major',
              help='Bumps the latest tag\'s major field')
@click.option('-m', '--minor', 'target', flag_value='minor',
              help='Bumps the latest tag\'s minor field')
@click.option('-p', '--patch', 'target', flag_value='patch',
              help='Bumps the latest tag\'s patch field')
@click.option('-l', '--label', default=None, type=str,
              help='Bumps the revision number for the given label')
def main(target, label):
    """
    Semver tag triggered deployment helper
    """
    check_environment(target, label)

    click.secho('Fetching tags from the upstream ...')
    handler = TagHandler(git.list_tags())

    print_information(handler, label)

    tag = handler.yield_tag(target, label)
    confirm(tag)


def check_environment(target, label):
    """
    Performs some environment checks prior to the program's execution
    """
    if not git.exists():
        click.secho('You must have git installed to use yld.', fg='red')
        sys.exit(1)

    if not os.path.isdir('.git'):
        click.secho('You must cd into a git repository to use yld.', fg='red')
        sys.exit(1)

    if not git.is_committed():
        click.secho('You must commit or stash your work before proceeding.',
                    fg='red')
        sys.exit(1)

    if target is None and label is None:
        click.secho('You must specify either a target or a label.', fg='red')
        sys.exit(1)


def print_information(handler, label):
    """
    Prints latest tag's information
    """
    click.echo('=> Latest stable: {tag}'.format(
        tag=click.style(str(handler.latest_stable or 'N/A'), fg='yellow' if
                        handler.latest_stable else 'magenta')
    ))

    if label is not None:
        latest_revision = handler.latest_revision(label)
        click.echo('=> Latest relative revision ({label}): {tag}'.format(
            label=click.style(label, fg='blue'),
            tag=click.style(str(latest_revision or 'N/A'),
                                fg='yellow' if latest_revision else 'magenta')
        ))


def confirm(tag):
    """
    Prompts user before proceeding
    """
    click.echo()
    if click.confirm('Do you want to create the tag {tag}?'.format(
            tag=click.style(str(tag), fg='yellow')),
        default=True, abort=True):
        git.create_tag(tag)

    if click.confirm(
        'Do you want to push the tag {tag} into the upstream?'.format(
            tag=click.style(str(tag), fg='yellow')),
        default=True):
        git.push_tag(tag)
        click.echo('Done!')
    else:
        git.delete_tag(tag)
        click.echo('Aborted!')


if __name__ == '__main__':
    main()
