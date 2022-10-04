import dataclasses

import addict
import attrdict
import box
import dict2dot
import dotmap
import dotsi
import dotted_dict
import dotty_dict
import glom
import metadict
import prodict
import pytest
import scalpl
from dataclass_wizard import fromdict

import dotwiz
from benchmarks.models import MyClass


# Mark all benchmarks in this module, and assign them to the specified group.
#   use with: `pytest benchmarks -m getattr`
pytestmark = [pytest.mark.getattr,
              pytest.mark.benchmark(group='getattr')]


@pytest.fixture
def my_data():
    return {'a': 3, 'b': 1, 'c': {'aa': 33, 'bb': [{'x': 77}]}}


def test_dict_getitem(benchmark, my_data):
    o = my_data

    result = benchmark(lambda: o['c']['bb'][0]['x'])
    assert result == 77


def test_dataclass_instance_kwargs(benchmark, my_data):
    """Passing keyword arguments to a dataclass generated with `make_dataclass`"""

    # noinspection PyPep8Naming
    X = dataclasses.make_dataclass('X', my_data)
    instance = X(** my_data)

    # note: it looks like value for field `c` gets loaded as a `dict`,
    # perhaps since we pass in keyword arguments directly.
    result = benchmark(lambda: instance.c['bb'][0]['x'])
    assert result == 77


def test_dataclass_instance_fromdict(benchmark, my_data):
    """Test for accessing attributes from a nested dataclass schema"""
    instance = fromdict(MyClass, my_data)

    result = benchmark(lambda: instance.c.bb[0].x)
    assert result == 77


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


def test_dotwiz_getitem(benchmark, my_data):
    o = dotwiz.DotWiz(my_data)
    # print(o)

    result = benchmark(lambda: o['c']['bb'][0]['x'])
    assert result == 77


def test_dotwiz_plus(benchmark, my_data):
    o = dotwiz.DotWizPlus(my_data)
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


def test_dotted_dict_preserve_keys(benchmark, my_data):
    o = dotted_dict.PreserveKeysDottedDict(my_data)
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


def test_addict(benchmark, my_data):
    o = addict.Dict(my_data)
    # print(o)

    result = benchmark(lambda: o.c.bb[0].x)
    assert result == 77


def test_attrdict(benchmark, my_data):
    o = attrdict.AttrDict(my_data)
    # print(o)

    result = benchmark(lambda: o.c.bb[0].x)
    assert result == 77


def test_glom(benchmark, my_data):
    o = my_data
    # print(o)

    # bring out the function to be fair with other tests, since attribute
    # access might hurt slightly otherwise.
    glom_fn = glom.glom

    result = benchmark(lambda: glom_fn(o, 'c.bb.0.x'))
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


def test_scalpl(benchmark, my_data):
    o = scalpl.Cut(my_data)
    # print(o)

    result = benchmark(lambda: o['c.bb[0].x'])
    assert result == 77


def test_simple_namespace(benchmark, my_data, parse_to_ns):
    o = parse_to_ns(my_data)
    # print(o)

    result = benchmark(lambda: o.c.bb[0].x)
    assert result == 77
