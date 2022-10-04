import dataclasses

import addict
import attrdict
import box
import dict2dot
import dotmap
import dotsi
import dotted_dict
import dotty_dict
import metadict
import prodict
import pytest
import scalpl
from dataclass_wizard import fromdict

import dotwiz
from benchmarks.models import MyClass


# Mark all benchmarks in this module, and assign them to the specified group.
#   use with: `pytest benchmarks -m create`
pytestmark = [pytest.mark.create,
              pytest.mark.benchmark(group='create')]


@pytest.fixture
def my_data():
    return {'a': 3, 'b': 1, 'c': {'aa': 33, 'bb': [{'x': 77}]}}


def test_make_dataclass(benchmark, my_data):
    # noinspection PyPep8Naming
    X = benchmark(dataclasses.make_dataclass, 'X', my_data)

    assert dataclasses.is_dataclass(X)


def test_dataclass_instance_kwargs(benchmark, my_data):
    """Passing keyword arguments to a dataclass generated with `make_dataclass`"""

    # noinspection PyPep8Naming
    X = dataclasses.make_dataclass('X', my_data)

    instance = benchmark(X, **my_data)
    # print(instance)

    # note: it looks like value for field `c` gets loaded as a `dict`,
    # perhaps since we pass in keyword arguments directly.
    assert instance.c['bb'][0]['x'] == 77


def test_dataclass_instance_fromdict(benchmark, my_data):
    """Test for creating a dataclass instance from a nested dict"""
    instance = benchmark(fromdict, MyClass, my_data)
    # print(instance)

    assert instance.c.bb[0].x == 77


def test_box(benchmark, my_data):
    result = benchmark(box.Box, my_data)
    # print(result)

    assert result.c.bb[0].x == 77


def test_box_without_conversion(benchmark, my_data):
    result = benchmark(box.Box, my_data, conversion_box=False)
    # print(result)

    assert result.c.bb[0].x == 77


def test_dotwiz(benchmark, my_data):
    result = benchmark(dotwiz.DotWiz, my_data)
    # print(result)

    assert result.c.bb[0].x == 77


def test_dotwiz_without_check_lists(benchmark, my_data):
    result = benchmark(dotwiz.DotWiz, my_data, _check_lists=False)
    # print(result)

    # now similar to `dict2dot`, `dict`s nested within `lists` won't work
    # assert result.c.bb[0].x == 77

    # instead, dict access should work fine:
    assert result.c.bb[0]['x'] == 77


def test_dotwiz_without_check_types(benchmark, my_data):
    result = benchmark(dotwiz.DotWiz, my_data, _check_types=False)
    # print(result)

    # now, `dict`s and `lists` nested within the input `dict` won't work
    # assert result.c.bb[0].x == 77

    # instead, dict access should work fine:
    assert result.c['bb'][0]['x'] == 77


def test_make_dot_wiz(benchmark, my_data):
    result = benchmark(dotwiz.make_dot_wiz, my_data)
    # print(result)

    assert result.c.bb[0].x == 77


def test_dotwiz_plus(benchmark, my_data):
    result = benchmark(dotwiz.DotWizPlus, my_data)
    # print(result)

    assert result.c.bb[0].x == 77


def test_dotwiz_plus_without_check_lists(benchmark, my_data):
    result = benchmark(dotwiz.DotWizPlus, my_data, _check_lists=False)
    # print(result)

    # now similar to `dict2dot`, `dict`s nested within `lists` won't work
    # assert result.c.bb[0].x == 77

    # instead, dict access should work fine:
    assert result.c.bb[0]['x'] == 77


def test_make_dot_wiz_plus(benchmark, my_data):
    result = benchmark(dotwiz.make_dot_wiz_plus, my_data)
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


def test_dotted_dict_preserve_keys(benchmark, my_data):
    result = benchmark(dotted_dict.PreserveKeysDottedDict, my_data)
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

    # instead, looks like dict access works:
    assert result.c.bb[0]['x'] == 77


def test_addict(benchmark, my_data):
    result = benchmark(addict.Dict, my_data)
    # print(result)

    assert result.c.bb[0].x == 77


def test_attrdict(benchmark, my_data):
    result = benchmark(attrdict.AttrDict, my_data)
    # print(result)

    assert result.c.bb[0].x == 77


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

    # instead, looks like dict access works:
    assert result.c.bb[0]['x'] == 77


def test_scalpl(benchmark, my_data):
    result = benchmark(scalpl.Cut, my_data)
    # print(result)

    assert result['c.bb[0].x'] == 77


def test_simple_namespace(benchmark, my_data, parse_to_ns):
    result = benchmark(parse_to_ns, my_data)
    # print(result)

    assert result.c.bb[0].x == 77
