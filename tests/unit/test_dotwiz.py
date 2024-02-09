"""Tests for `dotwiz` package."""

import pytest

from dotwiz import *

from .conftest import CleanupGetAttr


def test_dot_wiz_with_basic_usage():
    """Confirm intended functionality of `DotWiz`"""
    dw = DotWiz({'key_1': [{'k': 'v'}],
                 'keyTwo': '5',
                 'key-3': 3.21})

    assert dw.key_1[0].k == 'v'
    assert dw.keyTwo == '5'
    assert dw['key-3'] == 3.21


def test_make_dot_wiz():
    """Confirm intended functionality of `make_dot_wiz`"""
    dd = make_dot_wiz([(1, 'test'), ('two', [{'hello': 'world'}])],
                      a=1, b='two', c={'d': [123]})

    assert repr(dd) == "✫(a=1, b='two', c=✫(d=[123]), 1='test', two=[✫(hello='world')])"
    assert dd.a == 1
    assert dd.b == 'two'
    assert dd[1] == 'test'
    assert dd.two == [DotWiz(hello='world')]
    assert dd.c.d[0] == 123

    dd.b = [1, 2, 3]
    assert dd.b == [1, 2, 3]


class TestDefaultForMissingKeys(CleanupGetAttr):

    def test_usage(self):
        """Basic usage of :func:`set_default_for_missing_keys`."""
        set_default_for_missing_keys()

        dw = DotWiz(HelloWorld=True)
        assert dw.HelloWorld
        assert dw.world is None

    def test_overwrite(self):
        """
        Error is not raised when classes define a __getattr__()
        and ``overwrite=True`` is passed.
        """
        set_default_for_missing_keys('hello world')
        set_default_for_missing_keys(123, overwrite=True)

        assert DotWiz().missing_key == 123

    def test_overwrite_raises_an_error_by_default(self):
        """Error is raised when classes already define a __getattr__()."""
        set_default_for_missing_keys('test')

        with pytest.raises(ValueError) as e:
            set_default_for_missing_keys(None)

        # confirm that error message correctly indicates the fix/resolution
        assert 'pass `overwrite=True`' in str(e.value)


def test_dotwiz_init():
    """Confirm intended functionality of `DotWiz.__init__`"""
    dd = DotWiz({
        1: 'test',
        'two': [{'hello': 'world'}],
        'a': 1,
        'b': 'two',
        'c': {'d': [123]}
    })

    assert repr(dd) == "✫(1='test', two=[✫(hello='world')], a=1, b='two', c=✫(d=[123]))"
    assert dd.a == 1
    assert dd.b == 'two'
    assert dd[1] == 'test'
    assert dd.two == [DotWiz(hello='world')]
    assert dd.c.d[0] == 123

    dd.b = [1, 2, 3]
    assert dd.b == [1, 2, 3]


def test_dotwiz_del_attr():
    dd = DotWiz(
        a=1,
        b={'one': [1],
           'two': [{'first': 'one', 'second': 'two'}]},
        three={'four': [{'five': '5'}]}
    )

    assert dd.a == 1
    assert 'a' in dd

    del dd.a

    # note: it's currently expected that `hasattr` will not work, i.e.
    #   assert not hasattr(dd, 'a')
    assert 'a' not in dd

    assert isinstance(dd.b, DotWiz)
    assert dd.b.two[0].second == 'two'
    del dd.b.two[0].second
    assert 'second' not in dd.b.two[0]

    del dd.b
    assert 'b' not in dd


def test_dotwiz_get_attr():
    """Confirm intended functionality of `DotWiz.__getattr__`"""
    dd = DotWiz()
    dd.a = [{'one': 1, 'two': {'key': 'value'}}]

    item = getattr(dd, 'a')[0]
    assert isinstance(item, DotWiz)
    assert getattr(item, 'one') == 1

    assert getattr(getattr(item, 'two'), 'key') == 'value'
    # alternate way of writing the above
    assert item.two.key == 'value'


def test_dotwiz_get_item():
    """Confirm intended functionality of `DotWiz.__getitem__`"""
    dd = DotWiz()
    dd.a = [{'one': 1, 'two': {'key': 'value'}}]

    item = dd['a'][0]
    assert isinstance(item, DotWiz)
    assert item['one'] == 1

    assert item['two']['key'] == 'value'


def test_dotwiz_set_attr():
    """Confirm intended functionality of `DotWiz.__setattr__`"""
    dd = DotWiz()
    dd.a = [{'one': 1, 'two': 2}]

    item = dd.a[0]
    assert isinstance(item, DotWiz)
    assert item.one == 1
    assert item.two == 2


def test_dotwiz_set_item():
    """Confirm intended functionality of `DotWiz.__setitem__`"""
    dd = DotWiz()
    dd['a'] = [{'one': 1, 'two': 2}]

    item = dd.a[0]
    assert isinstance(item, DotWiz)
    assert item.one == 1
    assert item.two == 2


def test_dotwiz_update():
    """Confirm intended functionality of `DotWiz.update`"""
    dd = DotWiz(a=1, b={'one': [1]})
    assert isinstance(dd.b, DotWiz)

    dd.b.update({'two': [{'first': 'one', 'second': 'two'}]},
                three={'four': [{'five': '5'}]})

    assert isinstance(dd.b, DotWiz)
    assert isinstance(dd.b.two[0], DotWiz)
    assert isinstance(dd.b.three, DotWiz)
    assert dd.b.one == [1]

    item = dd.b.two[0]
    assert isinstance(item, DotWiz)
    assert item.first == 'one'
    assert item.second == 'two'

    item = dd.b.three.four[0]
    assert isinstance(item, DotWiz)
    assert item.five == '5'


def test_dotwiz_update_with_no_args():
    """Add for full branch coverage."""
    dd = DotWiz(a=1, b={'one': [1]})

    dd.update()
    assert dd.a == 1

    dd.update(a=2)
    assert dd.a == 2


def test_dotwiz_to_dict():
    """Confirm intended functionality of `DotWiz.to_dict`"""
    dw = DotWiz(hello=[{"key": "value", "another-key": {"a": "b"}}])

    assert dw.to_dict() == {
        'hello': [
            {
                'key': 'value',
                'another-key': {'a': 'b'}
            }
        ]
    }


def assert_raises(fn, typ):
    try:
        fn()
    except typ:
        return
    except Exception as e:
        assert False, f"expected {typ}, got {type(e)}"
    assert False, f"expected {typ}, got no exception"


def test_del():
    # https://github.com/rnag/dotwiz/issues/24
    d = DotWiz()
    d.a1 = 1
    d.a2 = 2
    assert d.get("a1")==1
    assert d.get("bad") is None
    assert d.get("bad", 3) == 3
    assert str(d)=="✫(a1=1, a2=2)"
    assert repr(d)=="✫(a1=1, a2=2)"
    assert repr(d.__dict__)=="{'a1': 1, 'a2': 2}"
    del d.a1
    assert repr(d)=="✫(a2=2)"
    assert_raises(lambda: d.a1, AttributeError)
    assert_raises(lambda: d['a1'], KeyError)
    # print(dir(d))
    assert d.__dict__ == {'a2': 2}
    assert list(d.__dict__.keys()) == ['a2']
    assert list(d.keys()) == ['a2']
    assert list(d.values()) == [2]

    assert [a for a in d] == ['a2']
    assert [a for a in d.items()] == [('a2', 2)]

    d.a3 = DotWiz()
    d.a3.a4 = 4
