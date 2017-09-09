"""
yld.tag
~~~~~~~

This module contains the tag in-memory logic and representation.
"""
import re

_regex = re.compile(r'^v?(?P<major>\d+)\.'
                    r'(?P<minor>\d+)\.'
                    r'(?P<patch>\d+)'
                    r'(?:-(?P<label>[^\.]+)\.'
                    r'(?P<number>\d+))?$')


class Version:
    """
    Represents a semantic version's prefix

    It consists of a MAJOR, a MINOR and a PATCH
    """
    def __init__(self, major, minor, patch):
        self.major = major
        self.minor = minor
        self.patch = patch

    def __repr__(self):
        return 'v{major}.{minor}.{patch}'.format(
            major=self.major,
            minor=self.minor,
            patch=self.patch
        )

    def __eq__(self, other):
        return self.major == other.major and \
                self.minor == other.minor and \
                self.patch == other.patch

    def __lt__(self, other):
        return self.major < other.major or \
                (self.major == other.major and self.minor < other.minor) or \
                (self.major == other.major and self.minor == other.minor
                 and self.patch < other.patch)

    def clone(self):
        """
        Returns a copy of this object
        """
        return Version(self.major, self.minor, self.patch)

    def bump(self, target):
        """
        Bumps the Version given a target

        The target can be either MAJOR, MINOR or PATCH
        """
        if target == 'patch':
            return Version(self.major, self.minor, self.patch + 1)
        if target == 'minor':
            return Version(self.major, self.minor + 1, 0)
        if target == 'major':
            return Version(self.major + 1, 0, 0)
        return self.clone()


class Revision:
    """
    Represents a semantic version's suffix

    It consists of a LABEL and a NUMBER
    """
    def __init__(self, label, number):
        self.label = label
        self.number = number

    def __repr__(self):
        return '-{label}.{number}'.format(
            label=self.label,
            number=self.number
        )

    def __eq__(self, other):
        return self.label == other.label and self.number == other.number

    def __lt__(self, other):
        return self.label < other.label or \
                (self.label == other.label and self.number < other.number)

    def clone(self):
        """
        Returns a copy of this object
        """
        return Revision(self.label, self.number)

    def bump(self):
        """
        Bumps the Revision's number
        """
        return Revision(self.label, self.number + 1)


class Tag:
    """
    Represents a full semantic version
    """
    def __init__(self, major, minor, patch, label=None, number=None):
        self.version = Version(major, minor, patch)
        self.revision = Revision(label, number) \
                if label is not None \
                else None

    def __repr__(self):
        r = repr(self.version)
        if self.revision:
            r += repr(self.revision)
        return r

    def __eq__(self, other):
        if self.version != other.version:
            return False
        if self.revision is None and other.revision is None:
            return True
        if self.revision is None or other.revision is None:
            return False
        return self.revision == other.revision

    def __lt__(self, other):
        if self.version < other.version:
            return True
        if self.version == other.version:
            if self.revision is not None and other.revision is not None:
                return self.revision < other.revision
            if self.revision is None and other.revision is None:
                return False
            if self.revision is None:
                return False
            if other.revision is None:
                return True
        else:
            return False

    def clone(self):
        """
        Returns a copy of this object
        """
        t = Tag(self.version.major, self.version.minor, self.version.patch)
        if self.revision is not None:
            t.revision = self.revision.clone()
        return t

    def with_revision(self, label, number):
        """
        Returns a Tag with a given revision
        """
        t = self.clone()
        t.revision = Revision(label, number)
        return t

    @staticmethod
    def from_version(version):
        """
        Creates a Tag, given a Version
        """
        return Tag(version.major, version.minor, version.patch)

    @staticmethod
    def default():
        """
        Returns the default Tag (v0.0.0)
        """
        return Tag(0, 0, 0)

    @staticmethod
    def parse(s):
        """
        Parses a string into a Tag
        """
        try:
            m = _regex.match(s)
            t = Tag(int(m.group('major')),
                    int(m.group('minor')),
                    int(m.group('patch')))
            return t \
                    if m.group('label') is None \
                    else t.with_revision(m.group('label'), int(m.group('number')))
        except AttributeError:
            return None


class TagHandler:
    def __init__(self, raw_tags):
        self.entries = sorted(self._parse(raw_tags), reverse=True)
        self.latest_stable = next((t for t in self.entries \
                                   if t.revision is None), None)

    def _parse(self, raw_tags):
        return [t for t in [Tag.parse(rt) for rt in raw_tags] if t is not None]

    @property
    def _latest_stable(self):
        return self.latest_stable or Tag.default()

    def latest(self, target, label):
        """
        Returns the latest Tag given a target to bump and a label
        """
        tag = self._yield_from_target(target)
        return next((t for t in self.entries \
                     if t.version == tag.version and \
                     t.revision is not None and \
                     t.revision.label == label), None)

    def latest_revision(self, label):
        """
        Returns the latest Tag revision with a given label
        """
        return next((t for t in self.entries \
                     if t.revision is not None and \
                     t.revision.label == label and \
                     t.version == self._latest_stable.version), None)

    def _latest_revision(self, label):
        return self.latest_revision(label) or \
                self._latest_stable.with_revision(label, 0)

    def yield_tag(self, target=None, label=None):
        """
        Returns a new Tag containing the bumped target and/or the bumped label
        """
        if target is None and label is None:
            raise ValueError('`target` and/or `label` must be specified')
        if label is None:
            return self._yield_from_target(target)
        if target is None:
            return self._yield_from_label(label)
        return self._yield_from_target_and_label(target, label)

    def _yield_from_target(self, target):
        return Tag.from_version(self._latest_stable.version.bump(target))

    def _yield_from_label(self, label):
        t = self._latest_revision(label)
        r = t.revision.bump()
        return Tag.from_version(t.version).with_revision(r.label, r.number)

    def _yield_from_target_and_label(self, target, label):
        tag = self._yield_from_target(target)
        t = next((t for t in self.entries \
                     if t.version == tag.version and \
                     t.revision is not None and \
                     t.revision.label == label), None)
        return tag.with_revision(label, 1 if t is None \
                                 else t.revision.number + 1)

