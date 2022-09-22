"""Tests for the `DotWizPlus` class."""
from collections import OrderedDict, defaultdict
from copy import deepcopy
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


def test_init_with_skip_init():
    """Confirm intended functionality of `DotWizPlus.__init__` with `_skip_init`"""
    # adding a constructor call with empty params, for comparison
    dw = DotWizPlus()
    assert dw.__dict__ == dw.__orig_dict__ == dw.__orig_keys__ == {}

    # now call the constructor with `_skip_init=True`
    dw = DotWizPlus(_skip_init=True)

    assert dw.__dict__ == {}

    # assert that attributes aren't present in the `DotWizPlus` object
    assert not hasattr(dw, '__orig_dict__')
    assert not hasattr(dw, '__orig_keys__')


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
           'two': [{'first': 'one', 'secondKey': 'two'}]},
        three={'four': [{'five': '5'}]}
    )

    assert dd.a == 1
    assert 'a' in dd

    del dd.a

    # note: it's currently expected that `hasattr` will not work, i.e.
    #   assert not hasattr(dd, 'a')
    assert 'a' not in dd

    assert isinstance(dd.b, DotWizPlus)
    assert dd.b.two[0].second_key == 'two'

    assert 'secondKey' in dd.b.two[0]
    del dd.b.two[0].second_key
    assert 'secondKey' not in dd.b.two[0]

    del dd.b
    assert 'b' not in dd


def test_get_attr():
    """Confirm intended functionality of `DotWizPlus.__getattr__`"""
    dd = DotWizPlus()
    dd.a = [{'one': 1, 'two': {'Inner-Key': 'value'}}]

    item = getattr(dd, 'a')[0]
    assert isinstance(item, DotWizPlus)
    assert getattr(item, 'one') == 1

    assert getattr(getattr(item, 'two'), 'inner_key') == 'value'
    # alternate way of writing the above
    assert item.two.inner_key == 'value'


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


@pytest.mark.parametrize("data,result", [({"a": 42}, True), ({}, False)])
def test_bool(data, result):
    dw = DotWizPlus(data)
    assert bool(dw) is result


def test_clear():
    dw = DotWizPlus({"a": 42})
    dw.clear()
    assert len(dw) == 0


def test_copy():
    data = {"a": 42}
    dw = DotWizPlus(data)
    assert dw.copy() == data


class TestEquals:

    def test_against_another_dot_wiz_plus(self):
        data = {"a": 42}
        dw = DotWizPlus(data)
        assert dw == DotWizPlus(data)

    def test_against_another_dict(self):
        data = {"a": 42}
        dw = DotWizPlus(data)
        assert dw == dict(data)

    def test_against_another_ordered_dict(self):
        data = {"a": 42}
        dw = DotWizPlus(data)
        assert dw == OrderedDict(data)

    def test_against_another_default_dict(self):
        data = {"a": 42}
        dw = DotWizPlus(data)
        assert dw == defaultdict(None, data)


class TestNotEquals:

    def test_against_another_dot_wiz_plus(self):
        data = {"a": 42}
        dw = DotWizPlus(a=41)
        assert dw != DotWizPlus(data)

    def test_against_another_dict(self):
        data = {"a": 42}
        dw = DotWizPlus(a=41)
        assert dw != dict(data)

    def test_against_another_ordered_dict(self):
        data = {"a": 42}
        dw = DotWizPlus(a=41)
        assert dw != OrderedDict(data)

    def test_against_another_default_dict(self):
        data = {"a": 42}
        dw = DotWizPlus(a=41)
        assert dw != defaultdict(None, data)


class TestFromKeys:
    def test_fromkeys(self):
        assert DotWizPlus.fromkeys(["Bulbasaur", "The-Charmander", "Squirtle"]) == DotWizPlus(
            {"Bulbasaur": None, "The-Charmander": None, "Squirtle": None}
        )

    def test_fromkeys_with_default_value(self):
        assert DotWizPlus.fromkeys(["Bulbasaur", "Charmander", "Squirtle"], "captured") == DotWizPlus(
            {"Bulbasaur": "captured", "Charmander": "captured", "Squirtle": "captured"}
        )

        dw = DotWizPlus.fromkeys(['class', 'lambda', '123'], 'Value')
        assert dw.class_ == dw.lambda_ == dw._123 == 'Value'


def test_items():
    dw = DotWizPlus({"a": 1, "secondKey": 2, "lambda": 3})
    assert sorted(dw.items()) == [("a", 1), ("lambda", 3), ("secondKey", 2)]


def test_iter():
    dw = DotWizPlus({"a": 1, "secondKey": 2, "c": 3})
    assert sorted([key for key in dw]) == ["a", "c", "secondKey"]


def test_keys():
    dw = DotWizPlus({"a": 1, "secondKey": 2, "c": 3})
    assert sorted(dw.keys()) == ["a", "c", "secondKey"]


def test_values():
    dw = DotWizPlus({"a": 1, "b": 2, "c": 3})
    assert sorted(dw.values()) == [1, 2, 3]


def test_len():
    dw = DotWizPlus({"a": 1, "b": 2, "c": 3})
    assert len(dw) == 3


def test_reversed():
    dw = DotWizPlus({"a": 1, "secondKey": 2, "c": 3})
    assert list(reversed(dw)) == ["c", "secondKey", "a"]


@pytest.mark.parametrize(
    "op1,op2,result",
    [
        (DotWizPlus(a=1, b=2), DotWizPlus(b=1.5, c=3), DotWizPlus({'a': 1, 'b': 1.5, 'c': 3})),
        (DotWizPlus(a=1, b=2), dict(b=1.5, c=3), DotWizPlus({'a': 1, 'b': 1.5, 'c': 3})),
    ],
)
def test_or(op1, op2, result):
    actual = op1 | op2

    assert type(actual) == type(result)
    assert actual == result


def test_ror():
    op1 = {'a': 1, 'b': 2}
    op2 = DotWizPlus(b=1.5, c=3)

    assert op1 | op2 == DotWizPlus({'a': 1, 'b': 1.5, 'c': 3})


# TODO: apparently __setitem__() or __or__() doesn't work with different cased
#   keys are used for the update. Will have to look into how to best handle this.
def test_ior():
    op1 = DotWizPlus(a=1, secondKey=2)
    op1 |= {'Second-Key': 1.5, 'c': 3}

    assert op1 == DotWizPlus({'a': 1, 'secondKey': 2, 'Second-Key': 1.5, 'c': 3})
    assert op1 != DotWizPlus({'a': 1, 'Second-Key': 1.5, 'c': 3})


def test_popitem():
    dw = DotWizPlus({"a": 1, "b": 2, "c": 3, "class": 4})

    assert len(dw) == len(dw.__dict__) == len(dw.__orig_dict__) == 4
    assert dw.__orig_keys__ == {'class_': 'class'}

    # items are returned in a LIFO (last-in, first-out) order
    (k, v) = dw.popitem()
    assert (k, v) == ('class', 4)

    assert len(dw) == len(dw.__dict__) == len(dw.__orig_dict__) == 3
    assert dw.__orig_keys__ == {}


@pytest.mark.parametrize(
    "data,key,result",
    [
        ({"this-key": 42}, "this-key", 42),
        ({"this-key": 42}, "this_key", None),
        ({"a": 42}, "b", None),
        # TODO: enable once we set up dot-style access
        # ({"a": {"b": 42}}, "a.b", 42),
        # ({"a": {"b": {"c": 42}}}, "a.b.c", 42),
        # ({"a": [42]}, "a[0]", 42),
        # ({"a": [{"b": 42}]}, "a[0].b", 42),
        # ({"a": [42]}, "a[1]", None),
        # ({"a": [{"b": 42}]}, "a[1].b", None),
        # ({"a": {"b": 42}}, "a.c", None),
        # ({"a": {"b": {"c": 42}}}, "a.b.d", None),
    ],
)
def test_get(data, key, result):
    dw = DotWizPlus(data)
    assert dw.get(key) == result


@pytest.mark.parametrize(
    "data,key,default",
    [
        ({}, "b", None),
        ({"a": 42}, "b", "default"),
    ],
)
def test_with_default(data, key, default):
    dw = DotWizPlus(data)
    assert dw.get(key, default) == default


class TestDelitem:
    @pytest.mark.parametrize(
        "data,key",
        [
            ({"a": 42}, "a"),
            ({"a": 1, "b": 2}, "b"),
        ],
    )
    def test_delitem(self, data, key):
        dw = DotWizPlus(deepcopy(data))
        del dw[key]
        assert key not in dw

    def test_key_error(self):
        dw = DotWizPlus({"a": 1, "c": 3})
        with pytest.raises(KeyError):
            del dw["b"]

    @pytest.mark.parametrize(
        "data,key",
        [
            ({False: "a"}, False),
            ({1: "a", 2: "b"}, 2),
        ],
    )
    def test_type_error(self, data, key):
        dw = DotWizPlus(deepcopy(data))
        # raises `TypeError` internally, but delete is still successful
        del dw[key]
        assert key not in dw


class TestContains:
    @pytest.mark.parametrize(
        "data,key,result",
        [
            ({"MyKey": 42}, "MyKey", True),
            ({"MyKey": 42}, "my_key", False),
            ({"a": 42}, "b", False),
        ],
    )
    def test_contains(self, data, key, result):
        dw = DotWizPlus(data)
        assert (key in dw) is result


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
    dd = DotWizPlus(First_Key=1, b={'one': [1]})

    dd.update()
    assert dd.first_key == 1

    dd.update(firstKey=2)
    assert dd.first_key == 2


class TestPop:

    @pytest.mark.parametrize(
        "data,key,result",
        [
            ({"a": 42}, "a", 42),
            ({"a": 1, "b": 2}, "b", 2),
        ],
    )
    def test_pop(self, data, key, result):
        dw = DotWizPlus(deepcopy(data))
        assert dw.pop(key) == result
        assert key not in dw

    @pytest.mark.parametrize(
        "data,key,default",
        [
            ({}, "b", None),
            ({"a": 1}, "b", 42),
        ],
    )
    def test_with_default(self, data, key, default):
        dw = DotWizPlus(deepcopy(data))
        assert dw.pop(key, default) == default


class TestSetDefault:

    @pytest.mark.parametrize(
        "data,key,result",
        [
            ({"a": 42}, "a", 42),
            ({"a": 1}, "b", None),
            # ({"a": {"b": 42}}, "a.b", 42),
            # ({"a": {"b": {"c": 42}}}, "a.b.c", 42),
            # ({"a": [42]}, "a[0]", 42),
            # ({"a": [{"b": 42}]}, "a[0].b", 42),
            # ({"a": {"b": 1}}, "a.c", None),
            # ({"a": {"b": {"c": 1}}}, "a.b.d", None),
            # ({"a": [{"b": 1}]}, "a[0].c", None),
            # ({"a": {"b": {"c": 42}}}, "a.d.e.f", None),
        ],
    )
    def test_setdefault(self, data, key, result):
        dw = DotWizPlus(deepcopy(data))
        assert dw.setdefault(key) == result
        assert dw[key] == result

    @pytest.mark.parametrize(
        "data,key,default",
        [
            ({}, "b", None),
            ({"a": 1}, "b", "default"),
            # ({"a": {"b": 1}}, "a.c", "default"),
            # ({"a": {"b": {"c": 1}}}, "a.b.d", "default"),
            # ({"a": [{"b": 1}]}, "a[0].c", "default"),
            # ({"a": {"b": {"c": 42}}}, "a.d.e.f", "default"),
        ],
    )
    def test_with_default(self, data, key, default):
        dw = DotWizPlus(deepcopy(data))
        assert dw.setdefault(key, default) == default
        assert dw[key] == default


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
