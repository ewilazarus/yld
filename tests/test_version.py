from yld.version import Version, VersionCatalog

class TestVersion:
    def test_repr(self):
        assert repr(Version(0, 1, 0)) == 'v0.1.0'
        assert repr(Version(0, 1, 0, 'beta', 1)) == 'v0.1.0-beta.1'

    def test_parse(self):
        stable = Version(0, 1, 0)
        revision = Version(0, 1, 0, 'beta', 1)

        assert Version.parse('v0.1.0') == stable
        assert Version.parse('0.1.0') == stable
        assert Version.parse('v0.1.0-beta.1') == revision
        assert Version.parse('0.1.0-beta.1') == revision
        assert Version.parse('something-else') == None

    def test_default(self):
        assert Version.default() == Version(0, 0, 0)
        assert Version.default('beta') == Version(0, 0, 0, 'beta', 0)

    def test_comparison(self):
        assert Version(0, 0, 1) < Version(0, 0, 2)
        assert Version(0, 1, 0) < Version(0, 2, 0)
        assert Version(1, 0, 0) < Version(2, 0, 0)
        assert Version(0, 0, 1) < Version(0, 1, 0)
        assert Version(0, 1, 0) < Version(1, 0, 0)
        assert Version(0, 0, 1) < Version(0, 0, 1, 'beta')
        assert Version(0, 0, 1, 'beta') < Version(0, 0, 2)
        assert Version(0, 0, 1, 'alpha') < Version(0, 0, 1, 'beta')
        assert Version(0, 0, 1, 'alpha', 1) < Version(0, 0, 1, 'alpha', 2)
        assert Version(0, 0, 1, 'alpha', 2) < Version(0, 0, 1, 'beta')

    def test_equality(self):
        assert Version(0, 0, 1) == Version(0, 0, 1)
        assert Version(0, 1, 0) == Version(0, 1, 0)
        assert Version(1, 0, 0) == Version(1, 0, 0)
        assert Version(0, 0, 1) != Version(0, 0, 2)
        assert Version(0, 1, 0) != Version(0, 2, 0)
        assert Version(1, 0, 0) != Version(2, 0, 0)
        assert Version(0, 0, 1, 'beta') == Version(0, 0, 1, 'beta')
        assert Version(0, 1, 0, 'beta') == Version(0, 1, 0, 'beta')
        assert Version(1, 0, 0, 'beta') == Version(1, 0, 0, 'beta')
        assert Version(0, 0, 1) != Version(0, 0, 1, 'beta')
        assert Version(0, 1, 0) != Version(0, 1, 0, 'beta')
        assert Version(1, 0, 0) != Version(1, 0, 0, 'beta')
        assert Version(0, 0, 1, 'beta') != Version(0, 0, 1, 'alpha')
        assert Version(0, 0, 1, 'beta', 1) != Version(0, 0, 1, 'beta', 2)

    def test_bump(self):
        assert Version(0, 0, 1).bump('patch') == Version(0, 0, 2)
        assert Version(0, 0, 1).bump('minor') == Version(0, 1, 0)
        assert Version(0, 0, 1).bump('major') == Version(1, 0, 0)
        assert Version(0, 1, 0).bump('patch') == Version(0, 1, 1)
        assert Version(0, 1, 0).bump('minor') == Version(0, 2, 0)
        assert Version(0, 1, 0).bump('major') == Version(1, 0, 0)
        assert Version(1, 0, 0).bump('patch') == Version(1, 0, 1)
        assert Version(1, 0, 0).bump('minor') == Version(1, 1, 0)
        assert Version(1, 0, 0).bump('major') == Version(2, 0, 0)
        assert Version(0, 0, 1, 'beta', 1).bump('revision', 'beta') \
                == Version(0, 0, 1, 'beta', 2)
        assert Version(0, 0, 1, 'alpha', 1).bump('revision', 'beta') \
                != Version(0, 0, 1, 'alpha', 2)
        assert Version(0, 0, 1, 'dev', 1).bump('minor') == Version(0, 1, 0)
        assert Version(0, 0, 1).bump('revision', 'beta') \
                == Version(0, 0, 1, 'beta', 1)

    def test_copy(self):
        assert Version(0, 1, 0).copy() == Version(0, 1, 0)
        assert not (Version(0, 1, 0).copy() is Version(0, 1, 0))

    def test_root(self):
        assert Version(0, 1, 0).root == Version(0, 1, 0)
        assert Version(0, 1, 0, 'beta', 1).root == Version(0, 1, 0)

    def test_is_stable(self):
        assert Version(0, 1, 0).is_stable
        assert not Version(0, 1, 0, 'beta', 1).is_stable


class TestVersionCatalog:
    raw_versions = 'v0.1.0 v0.1.0-beta.1 v0.1.1 v0.2.0-beta.1 ' + \
                   'v0.2.0-alpha1 v0.2.0-alpha.2'.split(' ')

    def test_parse(self):
        pass

