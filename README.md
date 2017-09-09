# `yld`

`yld` (YIELD) aims to make [semver](http://semver.org) tag triggered
deployments, using Git, less tedious and repetitive.


## How it works

```
$ yld --help
Usage: yld [OPTIONS]

  Semver tag triggered deployment helper

Options:
  -M, --major       Bumps the latest tag's major field
  -m, --minor       Bumps the latest tag's minor field
  -p, --patch       Bumps the latest tag's patch field
  -l, --label TEXT  Bumps the revision number for the given label
  --help            Show this message and exit.
```

## Example

```
$ yld --minor --label beta
Fetching tags from the upstream ...
=> Latest stable: v0.1.2
=> Latest relative revision (beta): N/A

Do you want to create the tag v0.2.0-beta.1? [Y/n]:
Do you want to push the tag v0.2.0-beta.1 into the upstream? [Y/n]:
Done!
```

## Installation

```
$ pip install yld

```

**Note:** This is a Python 3 only package.
