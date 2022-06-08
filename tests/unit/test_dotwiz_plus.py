"""Tests for the `DotWizPlus` class."""

import pytest

from dotwiz import DotWizPlus, make_dot_wiz_plus


def test_dot_wiz_plus_with_basic_usage():
    """Confirm intended functionality of `DotWizPlus`"""
    dw = DotWizPlus({'Key_1': [{'k': 'v'}],
                     'keyTwo': '5',
                     'key-3': 3.21,
                     7: True,
                     r'Hello, good day t!@#$%^&*(){}\:<?>/~`o you!': 'value',
                     'class': 'MyClass'})
    # print(dw)

    assert dw.key_1[0].k == 'v'
    assert dw.key_two == '5'
    assert dw.key_3 == 3.21
    assert dw._7 is True
    assert dw.hello_good_day_t_o_you == 'value'
    assert dw.class_ == 'MyClass'


def test_make_dot_wiz_plus():
    """Confirm intended functionality of `make_dot_wiz_plus`"""
    dd = make_dot_wiz_plus([(1, 'test'), ('two', [{'hello': 'world'}])],
                           a=1, b='two', c={'d': [123]})

    assert repr(dd) == "✪(a=1, b='two', c=✪(d=[123]), _1='test', two=[✪(hello='world')])"
    assert dd.a == 1
    assert dd.b == 'two'
    assert dd[1] == 'test'
    assert dd.two == [DotWizPlus(hello='world')]
    assert dd.c.d[0] == 123

    dd.b = [1, 2, 3]
    assert dd.b == [1, 2, 3]


def test_dotwiz_plus_init():
    """Confirm intended functionality of `DotWizPlus.__init__`"""
    dd = DotWizPlus({
        1: 'test',
        'two': [{'hello': 'world'}],
        'a': 1,
        'b': 'two',
        'c': {'d': [123]}
    })

    assert repr(dd) == "✪(_1='test', two=[✪(hello='world')], a=1, b='two', c=✪(d=[123]))"
    assert dd.a == 1
    assert dd.b == 'two'
    assert dd[1] == 'test'
    assert dd.two == [DotWizPlus(hello='world')]
    assert dd.c.d[0] == 123

    dd.b = [1, 2, 3]
    assert dd.b == [1, 2, 3]


def test_dotwiz_plus_del_attr():
    dd = DotWizPlus(
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

    assert isinstance(dd.b, DotWizPlus)
    assert dd.b.two[0].second == 'two'
    del dd.b.two[0].second
    assert 'second' not in dd.b.two[0]

    del dd.b
    assert 'b' not in dd


def test_dotwiz_plus_get_attr():
    """Confirm intended functionality of `DotWizPlus.__getattr__`"""
    dd = DotWizPlus()
    dd.a = [{'one': 1, 'two': {'key': 'value'}}]

    item = getattr(dd, 'a')[0]
    assert isinstance(item, DotWizPlus)
    assert getattr(item, 'one') == 1

    assert getattr(getattr(item, 'two'), 'key') == 'value'
    # alternate way of writing the above
    assert item.two.key == 'value'


def test_dotwiz_plus_get_item():
    """Confirm intended functionality of `DotWizPlus.__getitem__`"""
    dd = DotWizPlus()
    dd.a = [{'one': 1, 'two': {'key': 'value'}}]

    item = dd['a'][0]
    assert isinstance(item, DotWizPlus)
    assert item['one'] == 1

    assert item['two']['key'] == 'value'


def test_dotwiz_plus_set_attr():
    """Confirm intended functionality of `DotWizPlus.__setattr__`"""
    dd = DotWizPlus()
    dd.a = [{'one': 1, 'two': 2}]

    item = dd.a[0]
    assert isinstance(item, DotWizPlus)
    assert item.one == 1
    assert item.two == 2


def test_dotwiz_plus_set_item():
    """Confirm intended functionality of `DotWizPlus.__setitem__`"""
    dd = DotWizPlus()
    dd['a'] = [{'one': 1, 'two': 2}]

    item = dd.a[0]
    assert isinstance(item, DotWizPlus)
    assert item.one == 1
    assert item.two == 2


def test_dotwiz_plus_update():
    """Confirm intended functionality of `DotWizPlus.update`"""
    dd = DotWizPlus(a=1, b={'one': [1]})
    assert isinstance(dd.b, DotWizPlus)

    dd.b.update({'two': [{'first': 'one', 'second': 'two'}]},
                three={'four': [{'five': '5'}]})

    assert isinstance(dd.b, DotWizPlus)
    assert isinstance(dd.b.two[0], DotWizPlus)
    assert isinstance(dd.b.three, DotWizPlus)
    assert dd.b.one == [1]

    item = dd.b.two[0]
    assert isinstance(item, DotWizPlus)
    assert item.first == 'one'
    assert item.second == 'two'

    item = dd.b.three.four[0]
    assert isinstance(item, DotWizPlus)
    assert item.five == '5'


def test_dotwiz_plus_update_with_no_args():
    """Add for full branch coverage."""
    dd = DotWizPlus(a=1, b={'one': [1]})

    dd.update()
    assert dd.a == 1

    dd.update(a=2)
    assert dd.a == 2


def test_dotwiz_plus_to_dict():
    """Confirm intended functionality of `DotWizPlus.to_dict`"""
    dw = DotWizPlus(hello=[{"Key": "value", "Another-KEY": {"a": "b"}}],
                    camelCased={r"th@#$%is.is.!@#$%^&*()a{}\:<?>/~`.T'e'\"st": True})

    assert dw.to_dict() == {
        'hello': [
            {
                'Another-KEY': {'a': 'b'},
                'Key': 'value',
            }
        ],
        'camelCased': {
            'th@#$%is.is.!@#$%^&*()a{}\\:<?>/~`.T\'e\'\\"st': True
        },
    }


def test_dotwiz_plus_to_attr_dict():
    """Confirm intended functionality of `DotWizPlus.to_dict`"""
    dw = DotWizPlus(hello=[{"Key": "value", "Another-KEY": {"a": "b"}}],
                    camelCased={r"th@#$%is.is.!@#$%^&*()a{}\:<?>/~`.T'e'\"st": True})

    assert dw.to_attr_dict() == {
        'hello': [
            {
                'another_key': {'a': 'b'},
                'key': 'value',
            }
        ],
        'camel_cased': {'th_is_is_a_t_e_st': True},
    }


def test_key_in_special_keys():
    """Test case when key to add is present in `__SPECIAL_KEYS`"""

    dw = DotWizPlus({'for': 'value', 'hi-there': 'test', '3D': True})
    # print(dw)
    assert dw.for_ == 'value'
    assert dw.hi_there == 'test'
    assert dw._3d

    dw = DotWizPlus({'3D': True})
    assert dw._3d
