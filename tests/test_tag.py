from yld.tag import Version, Revision, Tag, TagHandler

# Version
def test_version_creation():
    v = Version(0, 1, 0)
    assert v.major == 0
    assert v.minor == 1
    assert v.patch == 0

def test_version_repr():
    assert repr(Version(0, 1, 0)) == 'v0.1.0'

def test_version_equality():
    v1 = Version(0, 1, 0)
    v2 = Version(0, 1, 0)
    assert v1 == v2

    v3 = Version(0, 2, 0)
    assert v2 != v3

def test_version_comparison():
    v1 = Version(0, 0, 1)
    v2 = Version(0, 0, 2)
    assert v1 < v2

    v1 = Version(0, 0, 1)
    v2 = Version(0, 1, 0)
    assert v1 < v2

    v1 = Version(0, 0, 1)
    v2 = Version(1, 0, 0)
    assert v1 < v2

    v1 = Version(0, 1, 0)
    v2 = Version(0, 2, 0)
    assert v1 < v2

    v1 = Version(0, 1, 0)
    v2 = Version(1, 0, 0)
    assert v1 < v2

    v1 = Version(1, 0, 0)
    v2 = Version(2, 0, 0)
    assert v1 < v2

def test_version_clone():
    v1 = Version(0, 1, 0)
    v2 = v1.clone()
    assert v1 == v2
    assert not(v1 is v2)

def test_version_bump():
    v1 = Version(1, 1, 1)
    assert v1.bump('patch') == Version(1, 1, 2)
    assert v1.bump('minor') == Version(1, 2, 0)
    assert v1.bump('major') == Version(2, 0, 0)
    assert v1.bump('something-else') == Version(1, 1, 1)


# Revision
def test_revision_creation():
    r = Revision('beta', 1)
    assert r.label == 'beta'
    assert r.number == 1

def test_revision_repr():
    assert repr(Revision('beta', 1)) == '-beta.1'

def test_revision_equality():
    r1 = Revision('beta', 1)
    r2 = Revision('beta', 1)
    assert r1 == r2

    r3 = Revision('beta', 2)
    assert r2 != r3

    r4 = Revision('alpha', 1)
    assert r2 != r4

    r5 = Revision('alpha', 2)
    assert r2 != r5

def test_revision_comparison():
    r1 = Revision('beta', 1)
    r2 = Revision('beta', 2)
    assert r1 < r2

    r3 = Revision('alpha', 1)
    assert r3 < r1

    r4 = Revision('alpha', 2)
    assert r4 < r1

def test_revision_clone():
    r1 = Revision('beta', 1)
    r2 = r1.clone()
    assert r1 == r2
    assert not(r1 is r2)

def test_revisioni_bump():
    r1 = Revision('beta', 1)
    assert r1.bump() == Revision('beta', 2)


# Tag
def test_tag_creation():
    t = Tag(0, 1, 0)
    assert t.version.major == 0
    assert t.version.minor == 1
    assert t.version.patch == 0
    assert t.revision is None

    t = Tag(0, 1, 0, 'beta', 1)
    assert t.version.major == 0
    assert t.version.minor == 1
    assert t.version.patch == 0
    assert t.revision.label == 'beta'
    assert t.revision.number == 1

def test_tag_repr():
    assert repr(Tag(0, 1, 0)) == 'v0.1.0'
    assert repr(Tag(0, 1, 0, 'beta', 1)) == 'v0.1.0-beta.1'

def test_tag_equality():
    t1 = Tag(0, 1, 0)
    t2 = Tag(0, 1, 0)
    assert t1 == t2

    t3 = Tag(0, 2, 0)
    assert t1 != t3

    t4 = Tag(0, 1, 0, 'beta', 1)
    assert t1 != t4
    assert t4 != t1

    t5 = Tag(0, 1, 0, 'beta', 1)
    assert t4 == t5

    t6 = Tag(0, 1, 0, 'beta', 2)
    assert t5 != t6

def test_tag_comparison():
    t1 = Tag(0, 1, 0)
    t2 = Tag(0, 2, 0)
    assert t1 < t2

    t3 = Tag(0, 1, 0, 'beta', 1)
    assert t3 < t2

    t4 = Tag(0, 1, 0, 'beta', 2)
    assert t3 < t4

    t5 = Tag(0, 2, 0, 'beta', 1)
    assert t1 < t5

    t6 = Tag(0, 2, 0, 'dev', 1)
    assert t5 < t6

    t7 = Tag(0, 3, 0)
    assert t6 < t7

def test_tag_clone():
    t1 = Tag(0, 1, 0)
    t2 = t1.clone()
    assert t1 == t2
    assert not(t1 is t2)

    t3 = Tag(0, 1, 0, 'beta', 1)
    t4 = t3.clone()
    assert t3 == t4
    assert not(t3 is t4)

def test_tag_with_revision():
    t = Tag(0, 1, 0)
    assert t.with_revision('beta', 1) == Tag(0, 1, 0, 'beta', 1)

def test_tag_default():
    assert Tag.default() == Tag(0, 0, 0)

def test_tag_from_verison():
    assert Tag.from_version(Version(0, 1, 0)) == Tag(0, 1, 0)

def test_tag_parse():
    assert Tag.parse('v0.1.0') == Tag(0, 1, 0)
    assert Tag.parse('0.1.0') == Tag(0, 1, 0)
    assert Tag.parse('v0.1.0-beta.1') == Tag(0, 1, 0, 'beta', 1)
    assert Tag.parse('0.1.0-beta.1') == Tag(0, 1, 0, 'beta', 1)
    assert Tag.parse('something-else') is None


# TagHandler
raw_tags = [
    'v0.2.0',
    'something-else',
    'v0.1.0',
    'v0.1.0-beta.1',
    'v0.3.0-dev.1',
    'v0.3.0'
]

def test_tag_container_creation():
    th = TagHandler(raw_tags)
    assert th.entries == [
        Tag(0, 3, 0),
        Tag(0, 3, 0, 'dev', 1),
        Tag(0, 2, 0),
        Tag(0, 1, 0),
        Tag(0, 1, 0, 'beta', 1),
    ]

    th = TagHandler([])
    assert th.entries == []

def test_tag_container_latest_stable():
    th = TagHandler(raw_tags)
    assert th.latest_stable == Tag(0, 3, 0)

    th = TagHandler(['v0.1.0-beta.1'])
    assert th.latest_stable is None

def test_tag_container_latest_revision():
    th = TagHandler(raw_tags)
    assert th.latest_revision('dev') == Tag(0, 3, 0, 'dev', 1)
    assert th.latest_revision('beta') is None

def test_tag_container_yield_tag():
    th1 = TagHandler(raw_tags)
    th2 = TagHandler([])
    assert th1.yield_tag(target='patch') == Tag(0, 3, 1)
    assert th1.yield_tag(target='minor') == Tag(0, 4, 0)
    assert th1.yield_tag(target='major') == Tag(1, 0, 0)

    assert th2.yield_tag(target='patch') == Tag(0, 0, 1)
    assert th2.yield_tag(target='minor') == Tag(0, 1, 0)
    assert th2.yield_tag(target='major') == Tag(1, 0, 0)
    
    assert th1.yield_tag(label='beta') == Tag(0, 3, 0, 'beta', 1)
    assert th1.yield_tag(label='dev') == Tag(0, 3, 0, 'dev', 2)

    assert th2.yield_tag(label='beta') == Tag(0, 0, 0, 'beta', 1)

    assert th1.yield_tag(target='minor', label='beta') == Tag(0, 4, 0, 'beta', 1)
    assert th1.yield_tag(target='minor', label='dev') == Tag(0, 4, 0, 'dev', 1)


