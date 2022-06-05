import dataclasses

import box
import dict2dot
import dotmap
import dotsi
import dotted_dict
import dotty_dict
import metadict
import prodict
import pytest

import dotwiz


@pytest.fixture
def my_data():
    return {'a': 3, 'b': 1, 'c': {'aa': 33, 'bb': [{'x': 77}]}}


def test_make_dataclass(benchmark, my_data):
    # noinspection PyPep8Naming
    X = benchmark(dataclasses.make_dataclass, 'X', my_data)

    assert dataclasses.is_dataclass(X)


def test_dataclass_instance(benchmark, my_data):
    # noinspection PyPep8Naming
    X = dataclasses.make_dataclass('X', my_data)

    instance = benchmark(X, **my_data)
    assert instance.a == 3


def test_box(benchmark, my_data):
    result = benchmark(box.Box, my_data)
    # print(result)

    assert result.c.bb[0].x == 77


def test_dotwiz(benchmark, my_data):
    result = benchmark(dotwiz.DotWiz, my_data)
    # print(result)

    assert result.c.bb[0].x == 77


def test_make_dot_wiz(benchmark, my_data):
    result = benchmark(dotwiz.make_dot_wiz, my_data)
    # print(result)

    assert result.c.bb[0].x == 77


def test_dotmap(benchmark, my_data):
    result = benchmark(dotmap.DotMap, my_data)
    # print(result)

    assert result.c.bb[0].x == 77


def test_dotted_dict(benchmark, my_data):
    result = benchmark(dotted_dict.DottedDict, my_data)
    # print(result)

    assert result.c.bb[0].x == 77


def test_dotty_dict(benchmark, my_data):
    result = benchmark(dotty_dict.Dotty, my_data)
    # print(result)

    # the syntax here is actually slightly different, as per the docs
    assert result['c.bb.0.x'] == 77


def test_dotsi(benchmark, my_data):
    result = benchmark(dotsi.Dict, my_data)
    # print(result)

    assert result.c.bb[0].x == 77


def test_dict2dot(benchmark, my_data):
    result = benchmark(dict2dot.Dict2Dot, my_data)
    assert result.b == 1
    # the docs mention that `dict`s nested within `lists` won't work
    # assert result.c.bb[0].x == 77


def test_metadict(benchmark, my_data):
    result = benchmark(metadict.MetaDict, my_data)
    # print(result)

    assert result.c.bb[0].x == 77


def test_prodict(benchmark, my_data):
    result = benchmark(prodict.Prodict.from_dict, my_data)
    # print(result)

    assert result.b == 1
    # note: commenting this out as this doesn't work for nested `lists`,
    # since the inner `dict` contents are not converted to a `Prodict`
    # type, apparently.
    #
    # see also:
    #   https://github.com/ramazanpolat/prodict/issues/17
    #
    # assert result.c.bb[0].x == 77
