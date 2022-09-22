"""Tests for the `DotWizPlusSlim` class."""
from collections import OrderedDict, defaultdict
from copy import deepcopy
from datetime import datetime

import pytest

from dotwiz.plus_slim import DotWizPlusSlim, make_dot_wiz_plus


def test_basic_usage():
    """Confirm intended functionality of `DotWizPlusSlim`"""
    dw = DotWizPlusSlim({'Key_1': [{'k': 'v'}],
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
    assert dd.two == [DotWizPlusSlim(hello='world')]
    assert dd.c.d[0] == 123

    dd.b = [1, 2, 3]
    assert dd.b == [1, 2, 3]


def test_init():
    """Confirm intended functionality of `DotWizPlusSlim.__init__`"""
    dd = DotWizPlusSlim({
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
    assert dd.two == [DotWizPlusSlim(hello='world')]
    assert dd.c.d[0] == 123

    dd.b = [1, 2, 3]
    assert dd.b == [1, 2, 3]


def test_init_with_skip_init():
    """Confirm intended functionality of `DotWizPlusSlim.__init__` with `_skip_init`"""
    # call the constructor with `_skip_init=True`
    dw = DotWizPlusSlim(_skip_init=True)
    assert dw.__dict__ == {}


def test_class_get_item():
    """Using __class_get_item__() to subscript the types, i.e. DotWizPlusSlim[K, V]"""
    dw = DotWizPlusSlim[str, int](first_key=123, SecondKey=321)

    # type hinting and auto-completion for value (int) works for dict access
    assert dw['first_key'].real == 123

    # however, the same doesn't work for attribute access. i.e. `dw.second_key.`
    # doesn't result in any method auto-completion or suggestions.
    assert dw.second_key == 321


def test_del_attr():
    dd = DotWizPlusSlim(
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

    assert isinstance(dd.b, DotWizPlusSlim)
    assert dd.b.two[0].second_key == 'two'

    assert 'second_key' in dd.b.two[0]
    del dd.b.two[0].second_key
    assert 'second_key' not in dd.b.two[0]

    del dd.b
    assert 'b' not in dd


def test_get_attr():
    """Confirm intended functionality of `DotWizPlusSlim.__getattr__`"""
    dd = DotWizPlusSlim()
    dd.a = [{'one': 1, 'two': {'Inner-Key': 'value'}}]

    item = getattr(dd, 'a')[0]
    assert isinstance(item, DotWizPlusSlim)
    assert getattr(item, 'one') == 1

    assert getattr(getattr(item, 'two'), 'inner_key') == 'value'
    # alternate way of writing the above
    assert item.two.inner_key == 'value'


def test_get_item():
    """Confirm intended functionality of `DotWizPlusSlim.__getitem__`"""
    dd = DotWizPlusSlim()
    dd.a = [{'one': 1, 'two': {'any-key': 'value'}}]

    item = dd['a'][0]
    assert isinstance(item, DotWizPlusSlim)
    assert item['one'] == 1

    assert item.two.any_key == 'value'
    assert item['two']['any_key'] == 'value'


def test_set_attr():
    """Confirm intended functionality of `DotWizPlusSlim.__setattr__`"""
    dd = DotWizPlusSlim()
    dd.AnyOne = [{'one': 1, 'keyTwo': 2}]

    item = dd.AnyOne[0]
    assert isinstance(item, DotWizPlusSlim)
    assert item.one == 1
    assert item.key_two == 2


def test_set_item():
    """Confirm intended functionality of `DotWizPlusSlim.__setitem__`"""
    dd = DotWizPlusSlim()
    dd['AnyOne'] = [{'one': 1, 'keyTwo': 2}]

    item = dd.any_one[0]
    assert isinstance(item, DotWizPlusSlim)
    assert item.one == 1
    assert item.key_two == 2


@pytest.mark.parametrize("data,result", [({"a": 42}, True), ({}, False)])
def test_bool(data, result):
    dw = DotWizPlusSlim(data)
    assert bool(dw) is result


def test_clear():
    dw = DotWizPlusSlim({"a": 42})
    dw.clear()
    assert len(dw) == 0


def test_copy():
    data = {"a": 42}
    dw = DotWizPlusSlim(data)
    assert dw.copy() == data


class TestEquals:

    def test_against_another_dot_wiz_plus(self):
        data = {"a": 42}
        dw = DotWizPlusSlim(data)
        assert dw == DotWizPlusSlim(data)

    def test_against_another_dict(self):
        data = {"a": 42}
        dw = DotWizPlusSlim(data)
        assert dw == dict(data)

    def test_against_another_ordered_dict(self):
        data = {"a": 42}
        dw = DotWizPlusSlim(data)
        assert dw == OrderedDict(data)

    def test_against_another_default_dict(self):
        data = {"a": 42}
        dw = DotWizPlusSlim(data)
        assert dw == defaultdict(None, data)


class TestNotEquals:

    def test_against_another_dot_wiz_plus(self):
        data = {"a": 42}
        dw = DotWizPlusSlim(a=41)
        assert dw != DotWizPlusSlim(data)

    def test_against_another_dict(self):
        data = {"a": 42}
        dw = DotWizPlusSlim(a=41)
        assert dw != dict(data)

    def test_against_another_ordered_dict(self):
        data = {"a": 42}
        dw = DotWizPlusSlim(a=41)
        assert dw != OrderedDict(data)

    def test_against_another_default_dict(self):
        data = {"a": 42}
        dw = DotWizPlusSlim(a=41)
        assert dw != defaultdict(None, data)


class TestFromKeys:
    def test_fromkeys(self):
        assert DotWizPlusSlim.fromkeys(["Bulbasaur", "The-Charmander", "Squirtle"]) == DotWizPlusSlim(
            {"Bulbasaur": None, "The-Charmander": None, "Squirtle": None}
        )

    def test_fromkeys_with_default_value(self):
        assert DotWizPlusSlim.fromkeys(["Bulbasaur", "Charmander", "Squirtle"], "captured") == DotWizPlusSlim(
            {"Bulbasaur": "captured", "Charmander": "captured", "Squirtle": "captured"}
        )

        dw = DotWizPlusSlim.fromkeys(['class', 'lambda', '123'], 'Value')
        assert dw.class_ == dw.lambda_ == dw._123 == 'Value'


def test_items():
    dw = DotWizPlusSlim({"a": 1, "secondKey": 2, "lambda": 3})
    assert sorted(dw.items()) == [("a", 1), ("lambda_", 3), ("second_key", 2)]


def test_iter():
    dw = DotWizPlusSlim({"a": 1, "secondKey": 2, "c": 3})
    assert sorted([key for key in dw]) == ["a", "c", "second_key"]


def test_keys():
    dw = DotWizPlusSlim({"a": 1, "secondKey": 2, "c": 3})
    assert sorted(dw.keys()) == ["a", "c", "second_key"]


def test_values():
    dw = DotWizPlusSlim({"a": 1, "b": 2, "c": 3})
    assert sorted(dw.values()) == [1, 2, 3]


def test_len():
    dw = DotWizPlusSlim({"a": 1, "b": 2, "c": 3})
    assert len(dw) == 3


def test_reversed():
    dw = DotWizPlusSlim({"a": 1, "secondKey": 2, "c": 3})
    assert list(reversed(dw)) == ["c", "second_key", "a"]


@pytest.mark.parametrize(
    "op1,op2,result",
    [
        (DotWizPlusSlim(a=1, b=2), DotWizPlusSlim(b=1.5, c=3), DotWizPlusSlim({'a': 1, 'b': 1.5, 'c': 3})),
        (DotWizPlusSlim(a=1, b=2), dict(b=1.5, c=3), DotWizPlusSlim({'a': 1, 'b': 1.5, 'c': 3})),
    ],
)
def test_or(op1, op2, result):
    actual = op1 | op2

    assert type(actual) == type(result)
    assert actual == result


def test_ror():
    op1 = {'a': 1, 'b': 2}
    op2 = DotWizPlusSlim(b=1.5, c=3)

    assert op1 | op2 == DotWizPlusSlim({'a': 1, 'b': 1.5, 'c': 3})


def test_ior():
    op1 = DotWizPlusSlim(a=1, secondKey=2)
    op1 |= {'Second-Key': 1.5, 'c': 3}

    assert op1 == DotWizPlusSlim({'a': 1, 'Second-Key': 1.5, 'c': 3})
    assert op1 == DotWizPlusSlim({'a': 1, 'secondKey': 2, 'Second-Key': 1.5, 'c': 3})


def test_popitem():
    dw = DotWizPlusSlim({"a": 1, "b": 2, "c": 3, "class": 4})

    assert len(dw) == len(dw.__dict__) == 4

    # items are returned in a LIFO (last-in, first-out) order
    (k, v) = dw.popitem()
    assert (k, v) == ('class_', 4)

    assert len(dw) == len(dw.__dict__) == 3


@pytest.mark.parametrize(
    "data,key,result",
    [
        ({"this-key": 42}, "this-key", None),
        ({"this-key": 42}, "this_key", 42),
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
    dw = DotWizPlusSlim(data)
    assert dw.get(key) == result


@pytest.mark.parametrize(
    "data,key,default",
    [
        ({}, "b", None),
        ({"a": 42}, "b", "default"),
    ],
)
def test_with_default(data, key, default):
    dw = DotWizPlusSlim(data)
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
        dw = DotWizPlusSlim(deepcopy(data))
        del dw[key]
        assert key not in dw

    def test_key_error(self):
        dw = DotWizPlusSlim({"a": 1, "c": 3})
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
        dw = DotWizPlusSlim(deepcopy(data))
        # raises `TypeError` internally, but delete is still successful
        del dw[key]
        assert key not in dw


class TestContains:
    @pytest.mark.parametrize(
        "data,key,result",
        [
            ({"MyKey": 42}, "MyKey", False),
            ({"MyKey": 42}, "my_key", True),
            ({"a": 42}, "b", False),
        ],
    )
    def test_contains(self, data, key, result):
        dw = DotWizPlusSlim(data)
        assert (key in dw) is result


def test_update():
    """Confirm intended functionality of `DotWizPlusSlim.update`"""
    dd = DotWizPlusSlim(a=1, b={'one': [1]})
    assert isinstance(dd.b, DotWizPlusSlim)

    dd.b.update({'two': [{'first': 'one', 'second': 'two'}]},
                threeFour={'five': [{'six': '6'}]})

    assert isinstance(dd.b, DotWizPlusSlim)
    assert isinstance(dd.b.two[0], DotWizPlusSlim)
    assert isinstance(dd.b.three_four, DotWizPlusSlim)
    assert dd.b.one == [1]

    item = dd.b.two[0]
    assert isinstance(item, DotWizPlusSlim)
    assert item.first == 'one'
    assert item.second == 'two'

    item = dd.b.three_four.five[0]
    assert isinstance(item, DotWizPlusSlim)
    assert item.six == '6'


def test_update_with_no_args():
    """Add for full branch coverage."""
    dd = DotWizPlusSlim(First_Key=1, b={'one': [1]})

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
        dw = DotWizPlusSlim(deepcopy(data))
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
        dw = DotWizPlusSlim(deepcopy(data))
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
        dw = DotWizPlusSlim(deepcopy(data))
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
        dw = DotWizPlusSlim(deepcopy(data))
        assert dw.setdefault(key, default) == default
        assert dw[key] == default


def test_from_json():
    """Confirm intended functionality of `DotWizPlusSlim.from_json`"""

    dw = DotWizPlusSlim.from_json("""
    {
        "key": {"nested": "value"},
        "second-key": [3, {"nestedKey": true}]
    }
    """)

    assert dw == DotWizPlusSlim(
        {
            'key': {'nested': 'value'},
            'second-key': [3, {'nestedKey': True}]
        }
    )

    assert dw.second_key[1].nested_key


def test_from_json_with_filename(mock_file_open):
    """
    Confirm intended functionality of `DotWizPlusSlim.from_json` when `filename`
    is passed.
    """

    file_contents = """
    {
        "key": {"nested": "value"},
        "second-key": [3, {"nestedKey": true}]
    }
    """

    mock_file_open.read_data = file_contents

    dw = DotWizPlusSlim.from_json(filename='test.json')

    assert dw == DotWizPlusSlim(
        {
            'key': {'nested': 'value'},
            'second-key': [3, {'nestedKey': True}]
        }
    )

    assert dw.second_key[1].nested_key


def test_from_json_with_multiline(mock_file_open):
    """
    Confirm intended functionality of `DotWizPlusSlim.from_json` when `filename`
    is passed, and `multiline` is enabled.
    """

    file_contents = """
    {"key": {"nested": "value"}}
    {"second-key": [3, {"nestedKey": true}]}
    """

    mock_file_open.read_data = file_contents

    dw_list = DotWizPlusSlim.from_json(filename='test.json', multiline=True)

    assert dw_list == [DotWizPlusSlim(key={'nested': 'value'}),
                       DotWizPlusSlim({'second-key': [3, {'nestedKey': True}]})]

    assert dw_list[1].second_key[1].nested_key


def test_to_dict():
    """Confirm intended functionality of `DotWizPlusSlim.to_dict`"""
    dw = DotWizPlusSlim(hello=[{"Key": "value", "Another-KEY": {"a": "b"}}],
                        camelCased={r"th@#$%is.is.!@#$%^&*()a{}\:<?>/~`.T'e'\"st": True})

    assert dw.to_dict() == {
        'hello': [
            {
                'another_key': {'a': 'b'},
                'key': 'value',
            }
        ],
        'camel_cased': {
            'th_is_is_a_t_e_st': True
        },
    }


def test_to_json():
    """Confirm intended functionality of `DotWizPlusSlim.to_json`"""
    dw = DotWizPlusSlim(hello=[{"Key": "value", "Another-KEY": {"a": "b"}}],
                        camelCased={r"th@#$%is.is.!@#$%^&*()a{}\:<?>/~`.T'e'\"st": True})

    assert dw.to_json(indent=4) == r"""
{
    "hello": [
        {
            "key": "value",
            "another_key": {
                "a": "b"
            }
        }
    ],
    "camel_cased": {
        "th_is_is_a_t_e_st": true
    }
}""".lstrip()


def test_to_json_with_filename(mock_file_open):
    """Confirm intended functionality of `DotWizPlusSlim.to_json` with `filename`"""
    dw = DotWizPlusSlim(hello=[{"Key": "value", "Another-KEY": {"a": "b"}}],
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
            "key": "value",
            "another_key": {
                "a": "b"
            }
        }
    ],
    "camel_cased": {
        "th_is_is_a_t_e_st": true
    }
}""".lstrip()


def test_key_in_special_keys():
    """Test case when key to add is present in `__SPECIAL_KEYS`"""

    dw = DotWizPlusSlim({'for': 'value', 'hi-there': 'test', '3D': True})
    # print(dw)
    assert dw.for_ == 'value'
    assert dw.hi_there == 'test'
    assert dw._3d

    dw = DotWizPlusSlim({'3D': True})
    assert dw._3d


def test_dir():
    """"Confirm intended functionality of `DotWizPlusSlim.__dir__`"""
    dw = DotWizPlusSlim({'1string': 'value', 'lambda': 42})

    obj_dir = dir(dw)

    assert 'keys' in obj_dir
    assert 'to_dict' in obj_dir

    assert '_1string' in obj_dir
    assert 'lambda_' in obj_dir

    assert '1string' not in obj_dir
    assert 'lambda' not in obj_dir


def test_to_json_with_non_serializable_type():
    """
    Confirm intended functionality of `DotWizPlusSlim.to_json` when an object
    doesn't define a `__dict__`, so the default `JSONEncoder.default`
    implementation is called.
    """

    dw = DotWizPlusSlim(string='val', dt=datetime.min)
    # print(dw)

    # TypeError: Object of type `datetime` is not JSON serializable
    with pytest.raises(TypeError):
        _ = dw.to_json()
