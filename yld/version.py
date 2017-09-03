"""
yld.version
~~~~~~~~~~~

This module contains the version in-memory logic and representation.
"""
import re

_TAG_REGEX = re.compile(r'^v?(?P<major>\d+)\.'
                       r'(?P<minor>\d+)\.'
                       r'(?P<patch>\d+)'
                       r'((?:-(?P<label>[^\.]+))'
                       r'(?:\.(?P<revision>\d+))?)?$')


class Version:
    """
    Version in-memory representation
    """
    def __init__(self, major, minor, patch, label=None, revision=None):
        self.major = major
        self.minor = minor
        self.patch = patch
        self.label = label
        if label is not None:
            self.revision = 0 if revision is None else int(revision)
        else:
            self.revision = None

    @staticmethod
    def parse(tag):
        """
        Parses a tag string into a Version
        """
        try:
            m = _TAG_REGEX.match(tag)
            return Version(int(m.group('major')), int(m.group('minor')),
                           int(m.group('patch')), m.group('label'),
                           int(m.group('revision')) \
                           if m.group('revision') else None)
        except AttributeError:
            return None

    @staticmethod
    def default(label=None):
        """
        Returns the default that is either v0.1.0 or v0.1.0-<label>.1
        """
        return Version(0, 1, 0, label)

    def __lt__(self, other):
        majors_eq = self.major == other.major
        minors_eq = self.minor == other.minor
        patches_eq = self.patch == other.patch

        mmp_lt = (self.major < other.major or
                  (majors_eq and self.minor < other.minor) or
                  (majors_eq and minors_eq and self.patch < other.patch))

        if mmp_lt:
            return True
        if not (majors_eq and minors_eq and patches_eq):
            return False
        if self.label is None and other.label is None:
            return False
        if self.label is None and other.label is not None:
            return True
        if self.label is not None and other.label is None:
            return False

        return (self.label < other.label or
                (self.label == other.label and self.revision < other.revision))

    def __eq__(self, other):
        return (self.major == other.major and
                self.minor == other.minor and
                self.patch == other.patch and
                self.label == other.label and
                self.revision == other.revision)

    def __repr__(self):
        repr = 'v{major}.{minor}.{patch}'.format(
            major=self.major,
            minor=self.minor,
            patch=self.patch)
        if self.label:
            repr += '-{label}.{revision}'.format(
                label=self.label,
                revision=self.revision)
        return repr

    @property
    def is_stable(self):
        """
        Returns 'True' if version is stable, otherwise 'False'
        """
        return self.label is None

    @property
    def root(self):
        """
        Returns the 'v{major}.{minor}.{patch}' root of the version
        """
        return Version(self.major, self.minor, self.patch)

    def copy(self):
        """
        Returns a copy of the current version
        """
        return Version(
            self.major, self.minor, self.patch, self.label, self.revision)

    def bump(self, mode, label=None):
        """
        Returns a copy with the incremented desired mode

        The desired mode should be either 'major', 'minor', 'patch' or
        'revision'
        """
        v = self.copy()
        if mode == 'major':
            v = Version(v.major + 1, 0, 0)
        elif mode == 'minor':
            v = Version(v.major, v.minor + 1, 0)
        elif mode == 'patch':
            v = Version(v.major, v.minor, v.patch + 1)
        elif mode == 'revision':
            if v.label is not None and v.label == label:
                v.revision += 1
            elif label is not None:
                v.label = label
                v.revision = 1
        return v


class VersionCatalog:
    """
    Version collection in-memory representation
    """
    def __init__(self, versions):
        self.versions = sorted([v for v in versions if v is not None],
                               reverse=True)

    @staticmethod
    def parse(tags):
        """
        Parses a list of tag strings into a VersionCatalog
        """
        return VersionCatalog([Version.parse(t) for t in tags])

    def stable_count(self):
        return len([v for v in self.versions if v.is_stable])

    def _latest(self):
        """
        Returns the latest root of the collection
        """
        return next((v.root.copy() for v in self.versions), Version.default())

    def _latest_stable(self):
        """
        Returns the latest stable of the colelction
        """
        return next((v.copy() \
                     for v in self.versions \
                     if v.is_stable), Version.default())

    def _latest_revision(self, label):
        """
        Returns the latest revision of the collection with the given label
        """
        l = self._latest()
        v = next((v.copy() \
                  for v in self.versions \
                  if v.label == label and v.root == l), None)
        if v is None:
            v = l
            v.bump('revision', label)
        return v

    def latest(self, label=None):
        """
        Returns the latest version of the collection

        The returner version will be either the latest stable or the latest
        revision, if a label was provided
        """
        return self._latest_stable() \
                if label is None \
                else self._latest_revision(label)

    def __len__(self):
        return len(self.versions)

    def __repr__(self):
        return repr(self.versions)

