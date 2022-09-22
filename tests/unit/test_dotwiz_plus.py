"""Tests for the `DotWizPlus` class."""
from datetime import datetime

import pytest

from dotwiz import *

from .conftest import CleanupGetAttr


def test_basic_usage():
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


class TestDefaultForMissingKeys(CleanupGetAttr):

    def test_usage(self):
        """Basic usage of :func:`set_default_for_missing_keys`."""
        set_default_for_missing_keys()

        dw = DotWizPlus(HelloWorld=True)
        assert dw.hello_world
        assert dw.world is None

    def test_overwrite(self):
        """
        Error is not raised when classes define a __getattr__()
        and ``overwrite=True`` is passed.
        """
        set_default_for_missing_keys('hello world')
        set_default_for_missing_keys(123, overwrite=True)

        assert DotWizPlus().missing_key == 123

    def test_overwrite_raises_an_error_by_default(self):
        """Error is raised when classes already define a __getattr__()."""
        set_default_for_missing_keys('test')

        with pytest.raises(ValueError) as e:
            set_default_for_missing_keys(None)

        # confirm that error message correctly indicates the fix/resolution
        assert 'pass `overwrite=True`' in str(e.value)


def test_init():
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


def test_class_get_item():
    """Using __class_get_item__() to subscript the types, i.e. DotWizPlus[K, V]"""
    dw = DotWizPlus[str, int](first_key=123, SecondKey=321)

    # type hinting and auto-completion for value (int) works for dict access
    assert dw['first_key'].real == 123

    # however, the same doesn't work for attribute access. i.e. `dw.second_key.`
    # doesn't result in any method auto-completion or suggestions.
    assert dw.second_key == 321


def test_del_attr():
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


def test_get_attr():
    """Confirm intended functionality of `DotWizPlus.__getattr__`"""
    dd = DotWizPlus()
    dd.a = [{'one': 1, 'two': {'key': 'value'}}]

    item = getattr(dd, 'a')[0]
    assert isinstance(item, DotWizPlus)
    assert getattr(item, 'one') == 1

    assert getattr(getattr(item, 'two'), 'key') == 'value'
    # alternate way of writing the above
    assert item.two.key == 'value'


def test_get_item():
    """Confirm intended functionality of `DotWizPlus.__getitem__`"""
    dd = DotWizPlus()
    dd.a = [{'one': 1, 'two': {'any-key': 'value'}}]

    item = dd['a'][0]
    assert isinstance(item, DotWizPlus)
    assert item['one'] == 1

    assert item.two.any_key == 'value'
    assert item['two']['any-key'] == 'value'


def test_set_attr():
    """Confirm intended functionality of `DotWizPlus.__setattr__`"""
    dd = DotWizPlus()
    dd.AnyOne = [{'one': 1, 'keyTwo': 2}]

    item = dd.AnyOne[0]
    assert isinstance(item, DotWizPlus)
    assert item.one == 1
    assert item.key_two == 2


def test_set_item():
    """Confirm intended functionality of `DotWizPlus.__setitem__`"""
    dd = DotWizPlus()
    dd['AnyOne'] = [{'one': 1, 'keyTwo': 2}]

    item = dd.any_one[0]
    assert isinstance(item, DotWizPlus)
    assert item.one == 1
    assert item.key_two == 2


def test_update():
    """Confirm intended functionality of `DotWizPlus.update`"""
    dd = DotWizPlus(a=1, b={'one': [1]})
    assert isinstance(dd.b, DotWizPlus)

    dd.b.update({'two': [{'first': 'one', 'second': 'two'}]},
                threeFour={'five': [{'six': '6'}]})

    assert isinstance(dd.b, DotWizPlus)
    assert isinstance(dd.b.two[0], DotWizPlus)
    assert isinstance(dd.b.three_four, DotWizPlus)
    assert dd.b.one == [1]

    item = dd.b.two[0]
    assert isinstance(item, DotWizPlus)
    assert item.first == 'one'
    assert item.second == 'two'

    item = dd.b.three_four.five[0]
    assert isinstance(item, DotWizPlus)
    assert item.six == '6'


def test_update_with_no_args():
    """Add for full branch coverage."""
    dd = DotWizPlus(a=1, b={'one': [1]})

    dd.update()
    assert dd.a == 1

    dd.update(a=2)
    assert dd.a == 2


def test_from_json():
    """Confirm intended functionality of `DotWizPlus.from_json`"""

    dw = DotWizPlus.from_json("""
    {
        "key": {"nested": "value"},
        "second-key": [3, {"nestedKey": true}]
    }
    """)

    assert dw == DotWizPlus(
        {
            'key': {'nested': 'value'},
            'second-key': [3, {'nestedKey': True}]
        }
    )

    assert dw.second_key[1].nested_key


def test_from_json_with_filename(mock_file_open):
    """
    Confirm intended functionality of `DotWizPlus.from_json` when `filename`
    is passed.
    """

    file_contents = """
    {
        "key": {"nested": "value"},
        "second-key": [3, {"nestedKey": true}]
    }
    """

    mock_file_open.read_data = file_contents

    dw = DotWizPlus.from_json(filename='test.json')

    assert dw == DotWizPlus(
        {
            'key': {'nested': 'value'},
            'second-key': [3, {'nestedKey': True}]
        }
    )

    assert dw.second_key[1].nested_key


def test_from_json_with_multiline(mock_file_open):
    """
    Confirm intended functionality of `DotWizPlus.from_json` when `filename`
    is passed, and `multiline` is enabled.
    """

    file_contents = """
    {"key": {"nested": "value"}}
    {"second-key": [3, {"nestedKey": true}]}
    """

    mock_file_open.read_data = file_contents

    dw_list = DotWizPlus.from_json(filename='test.json', multiline=True)

    assert dw_list == [DotWizPlus(key={'nested': 'value'}),
                       DotWizPlus({'second-key': [3, {'nestedKey': True}]})]

    assert dw_list[1].second_key[1].nested_key


def test_to_dict():
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


def test_to_dict_with_snake_cased_keys():
    """Confirm intended functionality of `DotWizPlus.to_dict` with `snake=True`"""
    dw = DotWizPlus(hello=[{"items": "value", "Another-KEY": {"for": {"123": True}}}],
                    camelCased={r"th@#$%is.is.!@#$%^&*()a{}\:<?>/~`.T'e'\"st": True})

    assert dw.to_dict(snake=True) == {
        'hello': [
            {
                'another_key': {
                    'for': {
                        '123': True
                    }
                },
                'items': 'value',
            }
        ],
        'camel_cased': {
            'th_is_is_a_t_e_st': True
        },
    }


def test_to_json():
    """Confirm intended functionality of `DotWizPlus.to_json`"""
    dw = DotWizPlus(hello=[{"Key": "value", "Another-KEY": {"a": "b"}}],
                    camelCased={r"th@#$%is.is.!@#$%^&*()a{}\:<?>/~`.T'e'\"st": True})

    assert dw.to_json(indent=4) == r"""
{
    "hello": [
        {
            "Key": "value",
            "Another-KEY": {
                "a": "b"
            }
        }
    ],
    "camelCased": {
        "th@#$%is.is.!@#$%^&*()a{}\\:<?>/~`.T'e'\\\"st": true
    }
}""".lstrip()


def test_to_json_with_attribute_keys():
    """Confirm intended functionality of `DotWizPlus.to_json` with `attr=True`"""
    dw = DotWizPlus(hello=[{"items": "value", "Another-KEY": {"for": {"123": True}}}],
                    camelCased={r"th@#$%is.is.!@#$%^&*()a{}\:<?>/~`.T'e'\"st": True})

    assert dw.to_json(attr=True, indent=4) == r"""
{
    "hello": [
        {
            "items_": "value",
            "another_key": {
                "for_": {
                    "_123": true
                }
            }
        }
    ],
    "camel_cased": {
        "th_is_is_a_t_e_st": true
    }
}""".lstrip()


def test_to_json_with_snake_cased_keys():
    """Confirm intended functionality of `DotWizPlus.to_json` with `snake=True`"""
    dw = DotWizPlus(hello=[{"items": "value", "Another-KEY": {"for": {"123": True}}}],
                    camelCased={r"th@#$%is.is.!@#$%^&*()a{}\:<?>/~`.T'e'\"st": True})

    assert dw.to_json(snake=True, indent=4) == r"""
{
    "hello": [
        {
            "items": "value",
            "another_key": {
                "for": {
                    "123": true
                }
            }
        }
    ],
    "camel_cased": {
        "th_is_is_a_t_e_st": true
    }
}""".lstrip()


def test_to_json_with_filename(mock_file_open):
    """Confirm intended functionality of `DotWizPlus.to_json` with `filename`"""
    dw = DotWizPlus(hello=[{"Key": "value", "Another-KEY": {"a": "b"}}],
                    camelCased={r"th@#$%is.is.!@#$%^&*()a{}\:<?>/~`.T'e'\"st": True})

    mock_filename = 'out_file-TEST.json'

    # write out to dummy file
    assert dw.to_json(filename=mock_filename, indent=4) is None

    # assert open(...) is called with expected arguments
    mock_file_open.assert_called_once_with(
        mock_filename, 'w', encoding='utf-8', errors='strict',
    )

    # assert expected mock data is written out
    assert mock_file_open.write_lines == r"""
{
    "hello": [
        {
            "Key": "value",
            "Another-KEY": {
                "a": "b"
            }
        }
    ],
    "camelCased": {
        "th@#$%is.is.!@#$%^&*()a{}\\:<?>/~`.T'e'\\\"st": true
    }
}""".lstrip()


def test_to_attr_dict():
    """Confirm intended functionality of `DotWizPlus.to_dict`"""
    dw = DotWizPlus(hello=[{"items": "value", "Another-KEY": {"for": {"123": True}}}],
                    camelCased={r"th@#$%is.is.!@#$%^&*()a{}\:<?>/~`.T'e'\"st": True})

    assert dw.to_attr_dict() == {
        'hello': [
            {
                'another_key': {
                    'for_': {
                        '_123': True
                    }
                },
                'items_': 'value',
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


def test_dir():
    """"Confirm intended functionality of `DotWizPlus.__dir__`"""
    dw = DotWizPlus({'1string': 'value', 'lambda': 42})

    obj_dir = dir(dw)

    assert 'keys' in obj_dir
    assert 'to_attr_dict' in obj_dir

    assert '_1string' in obj_dir
    assert 'lambda_' in obj_dir

    assert '1string' not in obj_dir
    assert 'lambda' not in obj_dir


def test_to_json_with_non_serializable_type():
    """
    Confirm intended functionality of `DotWizPlus.to_json` when an object
    doesn't define a `__dict__`, so the default `JSONEncoder.default`
    implementation is called.
    """

    dw = DotWizPlus(string='val', dt=datetime.min)
    # print(dw)

    # TypeError: Object of type `datetime` is not JSON serializable
    with pytest.raises(TypeError):
        _ = dw.to_json()
