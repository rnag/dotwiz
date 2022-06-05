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


def test_dict_getitem(benchmark, my_data):
    o = my_data

    result = benchmark(lambda: o['c']['bb'][0]['x'])
    assert result == 77


def test_dataclass_instance(benchmark, my_data):
    # noinspection PyPep8Naming
    X = dataclasses.make_dataclass('X', my_data)
    instance = X(** my_data)

    result = benchmark(lambda: instance.a)
    assert result == 3


def test_box(benchmark, my_data):
    o = box.Box(my_data)
    # print(o)

    result = benchmark(lambda: o.c.bb[0].x)
    assert result == 77


def test_dotwiz(benchmark, my_data):
    o = dotwiz.DotWiz(my_data)
    # print(o)

    result = benchmark(lambda: o.c.bb[0].x)
    assert result == 77


def test_dotmap(benchmark, my_data):
    o = dotmap.DotMap(my_data)
    # print(o)

    result = benchmark(lambda: o.c.bb[0].x)
    assert result == 77


def test_dotted_dict(benchmark, my_data):
    o = dotted_dict.DottedDict(my_data)
    # print(o)

    result = benchmark(lambda: o.c.bb[0].x)
    assert result == 77


def test_dotty_dict(benchmark, my_data):
    o = dotty_dict.Dotty(my_data)
    # print(o)

    # the syntax here is actually slightly different, as per the docs
    result = benchmark(lambda: o['c.bb.0.x'])
    assert result == 77


def test_dotsi(benchmark, my_data):
    o = dotsi.Dict(my_data)
    # print(o)

    result = benchmark(lambda: o.c.bb[0].x)
    assert result == 77


def test_dict2dot(benchmark, my_data):
    o = dict2dot.Dict2Dot(my_data)
    # print(o)

    # fix: because `dicts` within nested `lists` aren't converted.
    #   https://github.com/nandoabreu/python-dict2dot/blob/main/dict2dot/__init__.py#L5
    o.c.bb[0] = dict2dot.Dict2Dot(o.c.bb[0])

    result = benchmark(lambda: o.c.bb[0].x)
    assert result == 77


def test_metadict(benchmark, my_data):
    o = metadict.MetaDict(my_data)
    # print(o)

    result = benchmark(lambda: o.c.bb[0].x)
    assert result == 77


def test_prodict(benchmark, my_data):
    o = prodict.Prodict.from_dict(my_data)
    # print(o)

    # fix: because `dicts` within nested `lists` aren't converted.
    #   https://github.com/ramazanpolat/prodict/issues/17
    o.c.bb[0] = prodict.Prodict.from_dict(o.c.bb[0])

    result = benchmark(lambda: o.c.bb[0].x)
    assert result == 77
