"""Tests for `dotwiz` package."""
from collections import OrderedDict, defaultdict
from copy import deepcopy
from datetime import datetime

import pytest

from dotwiz import DotWiz, make_dot_wiz


def test_basic_usage():
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


def test_init():
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


def test_del_attr():
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


def test_get_attr():
    """Confirm intended functionality of `DotWiz.__getattr__`"""
    dd = DotWiz()
    dd.a = [{'one': 1, 'two': {'key': 'value'}}]

    item = getattr(dd, 'a')[0]
    assert isinstance(item, DotWiz)
    assert getattr(item, 'one') == 1

    assert getattr(getattr(item, 'two'), 'key') == 'value'
    # alternate way of writing the above
    assert item.two.key == 'value'


def test_get_item():
    """Confirm intended functionality of `DotWiz.__getitem__`"""
    dd = DotWiz()
    dd.a = [{'one': 1, 'two': {'key': 'value'}}]

    item = dd['a'][0]
    assert isinstance(item, DotWiz)
    assert item['one'] == 1

    assert item['two']['key'] == 'value'


def test_set_attr():
    """Confirm intended functionality of `DotWiz.__setattr__`"""
    dd = DotWiz()
    dd.a = [{'one': 1, 'two': 2}]

    item = dd.a[0]
    assert isinstance(item, DotWiz)
    assert item.one == 1
    assert item.two == 2


def test_set_item():
    """Confirm intended functionality of `DotWiz.__setitem__`"""
    dd = DotWiz()
    dd['a'] = [{'one': 1, 'two': 2}]

    item = dd.a[0]
    assert isinstance(item, DotWiz)
    assert item.one == 1
    assert item.two == 2


@pytest.mark.parametrize("data,result", [({"a": 42}, True), ({}, False)])
def test_bool(data, result):
    dw = DotWiz(data)
    assert bool(dw) is result


def test_clear():
    dw = DotWiz({"a": 42})
    dw.clear()
    assert len(dw) == 0


def test_copy():
    data = {"a": 42}
    dw = DotWiz(data)
    assert dw.copy() == data


class TestEquals:

    def test_against_another_dot_wiz(self):
        data = {"a": 42}
        dw = DotWiz(data)
        assert dw == DotWiz(data)

    def test_against_another_dict(self):
        data = {"a": 42}
        dw = DotWiz(data)
        assert dw == dict(data)

    def test_against_another_ordered_dict(self):
        data = {"a": 42}
        dw = DotWiz(data)
        assert dw == OrderedDict(data)

    def test_against_another_default_dict(self):
        data = {"a": 42}
        dw = DotWiz(data)
        assert dw == defaultdict(None, data)


class TestNotEquals:

    def test_against_another_dot_wiz(self):
        data = {"a": 42}
        dw = DotWiz(a=41)
        assert dw != DotWiz(data)

    def test_against_another_dict(self):
        data = {"a": 42}
        dw = DotWiz(a=41)
        assert dw != dict(data)

    def test_against_another_ordered_dict(self):
        data = {"a": 42}
        dw = DotWiz(a=41)
        assert dw != OrderedDict(data)

    def test_against_another_default_dict(self):
        data = {"a": 42}
        dw = DotWiz(a=41)
        assert dw != defaultdict(None, data)


class TestFromkeys:
    def test_fromkeys(self):
        assert DotWiz.fromkeys(["Bulbasaur", "Charmander", "Squirtle"]) == DotWiz(
            {"Bulbasaur": None, "Charmander": None, "Squirtle": None}
        )

    def test_fromkeys_with_default_value(self):
        assert DotWiz.fromkeys(["Bulbasaur", "Charmander", "Squirtle"], "captured") == DotWiz(
            {"Bulbasaur": "captured", "Charmander": "captured", "Squirtle": "captured"}
        )


def test_items():
    dw = DotWiz({"a": 1, "b": 2, "c": 3})
    assert sorted(dw.items()) == [("a", 1), ("b", 2), ("c", 3)]


def test_iter():
    dw = DotWiz({"a": 1, "b": 2, "c": 3})
    assert sorted([key for key in dw]) == ["a", "b", "c"]


def test_keys():
    dw = DotWiz({"a": 1, "b": 2, "c": 3})
    assert sorted(dw.keys()) == ["a", "b", "c"]


def test_values():
    dw = DotWiz({"a": 1, "b": 2, "c": 3})
    assert sorted(dw.values()) == [1, 2, 3]


def test_len():
    dw = DotWiz({"a": 1, "b": 2, "c": 3})
    assert len(dw) == 3


def test_reversed():
    dw = DotWiz({"a": 1, "b": 2, "c": 3})
    assert list(reversed(dw)) == ["c", "b", "a"]


@pytest.mark.parametrize(
    "op1,op2,result",
    [
        (DotWiz(a=1, b=2), DotWiz(b=1.5, c=3), DotWiz({'a': 1, 'b': 1.5, 'c': 3})),
        (DotWiz(a=1, b=2), dict(b=1.5, c=3), DotWiz({'a': 1, 'b': 1.5, 'c': 3})),
    ],
)
def test_or(op1, op2, result):
    actual = op1 | op2

    assert type(actual) == type(result)
    assert actual == result


def test_ror():
    op1 = {'a': 1, 'b': 2}
    op2 = DotWiz(b=1.5, c=3)

    assert op1 | op2 == DotWiz({'a': 1, 'b': 1.5, 'c': 3})


def test_ior():
    op1 = DotWiz(a=1, b=2)
    op1 |= {'b': 1.5, 'c': 3}

    assert op1 == DotWiz(a=1, b=1.5, c=3)


def test_popitem():
    dw = DotWiz({"a": 1, "b": 2, "c": 3})
    dw.popitem()
    assert len(dw) == 2


@pytest.mark.parametrize(
    "data,key,result",
    [
        ({"a": 42}, "a", 42),
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
    dw = DotWiz(data)
    assert dw.get(key) == result


@pytest.mark.parametrize(
    "data,key,default",
    [
        ({}, "b", None),
        ({"a": 42}, "b", "default"),
    ],
)
def test_with_default(data, key, default):
    dw = DotWiz(data)
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
        dw = DotWiz(deepcopy(data))
        del dw[key]
        assert key not in dw

    def test_key_error(self):
        dw = DotWiz({"a": 1, "c": 3})
        # raises `AttributeError` currently, might want to return a `KeyError` instead though
        with pytest.raises(AttributeError):
            del dw["b"]

    @pytest.mark.parametrize(
        "data,key",
        [
            ({False: "a"}, False),
            ({1: "a", 2: "b"}, 2),
        ],
    )
    def test_type_error(self, data, key):
        dw = DotWiz(deepcopy(data))
        # raises `TypeError` internally, but delete is still successful
        del dw[key]
        assert key not in dw


class TestContains:
    @pytest.mark.parametrize(
        "data,key,result",
        [
            ({"a": 42}, "a", True),
            ({"a": 42}, "b", False),
        ],
    )
    def test_contains(self, data, key, result):
        dw = DotWiz(data)
        assert (key in dw) is result


def test_update():
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


def test_update_with_no_args():
    """Add for full branch coverage."""
    dd = DotWiz(a=1, b={'one': [1]})

    dd.update()
    assert dd.a == 1

    dd.update(a=2)
    assert dd.a == 2


class TestPop:

    @pytest.mark.parametrize(
        "data,key,result",
        [
            ({"a": 42}, "a", 42),
            ({"a": 1, "b": 2}, "b", 2),
        ],
    )
    def test_pop(self, data, key, result):
        dw = DotWiz(deepcopy(data))
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
        dw = DotWiz(deepcopy(data))
        assert dw.pop(key, default) == default


class TestSetdefault:

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
        dw = DotWiz(deepcopy(data))
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
        dw = DotWiz(deepcopy(data))
        assert dw.setdefault(key, default) == default
        assert dw[key] == default


def test_to_dict():
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


def test_to_json():
    """Confirm intended functionality of `DotWiz.to_json`"""
    dw = DotWiz(hello=[{"key": "value", "another-key": {"a": "b"}}])

    assert dw.to_json(indent=4) == """\
{
    "hello": [
        {
            "key": "value",
            "another-key": {
                "a": "b"
            }
        }
    ]
}"""


def test_to_json_with_non_serializable_type():
    """
    Confirm intended functionality of `DotWiz.to_json` when an object
    doesn't define a `__dict__`, so the default `JSONEncoder.default`
    implementation is called.
    """

    dw = DotWiz(string='val', dt=datetime.min)
    # print(dw)

    # TypeError: Object of type `datetime` is not JSON serializable
    with pytest.raises(TypeError):
        _ = dw.to_json()
