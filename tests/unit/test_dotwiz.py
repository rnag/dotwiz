"""Tests for `dotwiz` package."""

import pytest

from dotwiz import DotWiz, make_dot_wiz


def test_make_dot_wiz():
    """Confirm intended functionality of `make_dot_wiz`"""
    dd = make_dot_wiz({1: 'test', 'two': [{'hello': 'world'}]},
                      a=1, b='two', c={'d': [123]})

    assert repr(dd) == "DotWiz(a=1, b='two', c=DotWiz(d=[123]), 1='test', two=[DotWiz(hello='world')])"
    assert dd.a == 1
    assert dd.b == 'two'
    assert dd[1] == 'test'
    assert dd.two == [DotWiz(hello='world')]
    assert dd.c.d[0] == 123

    dd.b = [1, 2, 3]
    assert dd.b == [1, 2, 3]


def test_dotwiz_from_dict():
    """Confirm intended functionality of `DotWiz.from_dict`"""
    dd = DotWiz.from_dict({
        1: 'test',
        'two': [{'hello': 'world'}],
        'a': 1,
        'b': 'two',
        'c': {'d': [123]}
    })

    assert repr(dd) == "DotWiz(1='test', two=[DotWiz(hello='world')], a=1, b='two', c=DotWiz(d=[123]))"
    assert dd.a == 1
    assert dd.b == 'two'
    assert dd[1] == 'test'
    assert dd.two == [DotWiz(hello='world')]
    assert dd.c.d[0] == 123

    dd.b = [1, 2, 3]
    assert dd.b == [1, 2, 3]


def test_dotwiz_del_attr():
    dd = DotWiz.from_kwargs(
        a=1,
        b={'one': [1],
           'two': [{'first': 'one', 'second': 'two'}]},
        three={'four': [{'five': '5'}]}
    )
    assert dd.a == 1
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
    dd = DotWiz.from_kwargs(a=1, b={'one': [1]})
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
