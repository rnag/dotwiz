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
from dotwiz.plus_slim import DotWizPlusSlim

from benchmarks.models import MyClassSpecialCased


# Mark all benchmarks in this module, and assign them to the specified group.
#   use with: `pytest benchmarks -m create_with_special_keys`
#   use with: `pytest benchmarks -m create_sp`
pytestmark = [pytest.mark.create_with_special_keys,
              # alias, for easier typing
              pytest.mark.create_sp,
              pytest.mark.benchmark(group='create_with_special_keys')]


@pytest.fixture
def my_data():
    return {'camelCase': 1,
            'Snake_Case': 2,
            'PascalCase': 3,
            'spinal-case3': 4,
            'Hello, how\'s it going?': 5,
            '3D': 6,
            'for': {'1nfinity': [{'and': {'Beyond!': 8}}]},
            'Some  r@ndom#$(*#@ Key##$# here   !!!': 'T'}


@pytest.fixture
def my_data_no_keywords():
    return {'camelCase': 1,
            'Snake_Case': 2,
            'PascalCase': 3,
            'spinal-case3': 4,
            'Hello, how\'s it going?': 5,
            '3D': 6,
            'for_': {'1nfinity': [{'and_': {'Beyond!': 8}}]},
            'Some  r@ndom#$(*#@ Key##$# here   !!!': 'T'}


# note: `make_dataclass` doesn't work because the keys aren't valid identifiers
# def test_dataclass_instance(benchmark, my_data):
#     # noinspection PyPep8Naming
#     X = dataclasses.make_dataclass('X', my_data)
#
#     instance = benchmark(X, **my_data)
#     assert instance.a == 3


def assert_eq(result):
    assert result.camelCase == 1
    assert result.Snake_Case == 2
    assert result.PascalCase == 3
    assert result.spinal_case3 == 4
    assert result['Hello, how\'s it going?'] == 5
    assert result['3D'] == 6
    assert result['for']['1nfinity'][0]['and']['Beyond!'] == 8
    assert result['Some  r@ndom#$(*#@ Key##$# here   !!!'] == 'T'


def assert_eq2(result):
    assert result.camelCase == 1
    assert result.Snake_Case == 2
    assert result.PascalCase == 3
    assert result['spinal-case3'] == 4
    assert result['Hello, how\'s it going?'] == 5
    assert result['3D'] == 6
    assert result['for']['1nfinity'][0]['and']['Beyond!'] == 8
    assert result['Some  r@ndom#$(*#@ Key##$# here   !!!'] == 'T'


def assert_eq3(result, nested_in_dict=True, nested_in_list=True):
    assert result.camel_case == 1
    assert result.snake_case == 2
    assert result.pascal_case == 3
    assert result.spinal_case3 == 4
    assert result.hello_how_s_it_going == 5
    assert result._3d == 6
    if nested_in_list:
        assert result.for_._1nfinity[0].and_.beyond == 8
    elif nested_in_dict:
        assert result.for_._1nfinity[0]['and']['Beyond!'] == 8
    else:
        assert result.for_['1nfinity'][0]['and']['Beyond!'] == 8
    assert result.some_r_ndom_key_here == 'T'


def assert_eq4(result):
    assert result.camelCase == 1
    assert result.Snake_Case == 2
    assert result.PascalCase == 3
    assert result.spinal_case3 == 4
    assert result.Hello__how_s_it_going_ == 5
    assert result._3D == 6
    assert result.for_._1nfinity[0].and_.Beyond_ == 8
    assert result.Some__r_ndom_______Key_____here______ == 'T'


def assert_eq5(result, subscript_list=False):
    assert result['camelCase'] == 1
    assert result['Snake_Case'] == 2
    assert result['PascalCase'] == 3
    assert result['spinal-case3'] == 4
    assert result['Hello, how\'s it going?'] == 5
    assert result['3D'] == 6
    key = 'for.1nfinity[0].and.Beyond!' if subscript_list else 'for.1nfinity.0.and.Beyond!'
    assert result[key] == 8
    assert result['Some  r@ndom#$(*#@ Key##$# here   !!!'] == 'T'


def assert_eq6(result: MyClassSpecialCased):
    """For testing with :class:`MyClassSpecialCased` from :mod:`models.py`"""
    assert result.camel_case == 1
    assert result.snake_case == 2
    assert result.pascal_case == 3
    assert result.spinal_case3 == 4
    assert result.hello == 5
    assert result._3d == 6
    assert result.for_.infinity[0].and_.beyond == 8
    assert result.some_random_key_here == 'T'


def assert_eq7(result, ns_to_dict):
    """For testing with a `types.SimpleNamespace` object, primarily"""
    assert result.camelCase == 1
    assert result.Snake_Case == 2
    assert result.PascalCase == 3

    result_dict = ns_to_dict(result)

    assert result_dict['spinal-case3'] == 4
    assert result_dict['Hello, how\'s it going?'] == 5
    assert result_dict['3D'] == 6
    assert result_dict['for']['1nfinity'][0]['and']['Beyond!'] == 8
    assert result_dict['Some  r@ndom#$(*#@ Key##$# here   !!!'] == 'T'


@pytest.mark.xfail(reason='some key names are not valid identifiers')
def test_make_dataclass(benchmark, my_data):
    # noinspection PyPep8Naming
    X = benchmark(dataclasses.make_dataclass, 'X', my_data)

    assert dataclasses.is_dataclass(X)


def test_dataclass_instance_fromdict(benchmark, my_data):
    """Test for creating a dataclass instance from a nested dict"""
    instance = benchmark(fromdict, MyClassSpecialCased, my_data)
    # print(instance)

    assert_eq6(instance)


def test_box(benchmark, my_data):
    result = benchmark(box.Box, my_data)
    # print(result)

    assert_eq(result)


def test_box_without_conversion(benchmark, my_data):
    result = benchmark(box.Box, my_data, conversion_box=False)
    # print(result)

    assert_eq2(result)


def test_dotwiz(benchmark, my_data):
    result = benchmark(dotwiz.DotWiz, my_data)
    # print(result)

    assert_eq2(result)


def test_dotwiz_without_check_lists(benchmark, my_data):
    result = benchmark(dotwiz.DotWiz, my_data, _check_lists=False)
    # print(result)

    assert_eq2(result)


def test_dotwiz_without_check_types(benchmark, my_data):
    result = benchmark(dotwiz.DotWiz, my_data, _check_types=False)
    # print(result)

    assert_eq2(result)


def test_make_dot_wiz(benchmark, my_data):
    result = benchmark(dotwiz.make_dot_wiz, my_data)
    # print(result)

    assert_eq2(result)


def test_dotwiz_plus_slim(benchmark, my_data):
    result = benchmark(DotWizPlusSlim, my_data)
    # print(result)

    assert_eq3(result)


def test_dotwiz_plus(benchmark, my_data):
    result = benchmark(dotwiz.DotWizPlus, my_data)
    # print(result)

    assert_eq3(result)


def test_dotwiz_plus_without_check_lists(benchmark, my_data):
    result = benchmark(dotwiz.DotWizPlus, my_data, _check_lists=False)
    # print(result)

    assert_eq3(result, nested_in_list=False)


def test_dotwiz_plus_without_check_types(benchmark, my_data):
    result = benchmark(dotwiz.DotWizPlus, my_data, _check_types=False)
    # print(result)

    assert_eq3(result, nested_in_list=False, nested_in_dict=False)


def test_make_dot_wiz_plus(benchmark, my_data):
    result = benchmark(dotwiz.make_dot_wiz_plus, my_data)
    # print(result)

    assert_eq3(result)


def test_dotmap(benchmark, my_data):
    result = benchmark(dotmap.DotMap, my_data)
    # print(result)

    assert_eq2(result)


def test_dotted_dict(benchmark, my_data_no_keywords):
    result = benchmark(dotted_dict.DottedDict, my_data_no_keywords)
    # print(result)

    assert_eq4(result)


def test_dotted_dict_preserve_keys(benchmark, my_data):
    result = benchmark(dotted_dict.PreserveKeysDottedDict, my_data)
    # print(result)

    assert_eq2(result)


def test_dotty_dict(benchmark, my_data):
    result = benchmark(dotty_dict.Dotty, my_data)
    # print(result)

    # the syntax here is actually slightly different, as per the docs
    assert_eq5(result)


def test_dotsi(benchmark, my_data):
    result = benchmark(dotsi.Dict, my_data)
    # print(result)

    assert_eq2(result)


def test_dict2dot(benchmark, my_data):
    result = benchmark(dict2dot.Dict2Dot, my_data)
    # print(result)

    # the docs mention that `dict`s nested within `lists` won't work
    # so, attribute access for those ones won't work
    assert_eq2(result)


def test_addict(benchmark, my_data):
    result = benchmark(addict.Dict, my_data)
    # print(result)

    assert_eq2(result)


def test_attrdict(benchmark, my_data):
    result = benchmark(attrdict.AttrDict, my_data)
    # print(result)

    assert_eq2(result)


def test_metadict(benchmark, my_data):
    result = benchmark(metadict.MetaDict, my_data)
    # print(result)

    assert_eq2(result)


def test_prodict(benchmark, my_data):
    result = benchmark(prodict.Prodict.from_dict, my_data)
    # print(result)

    # note: this doesn't work for nested `lists`, since the inner `dict
    # contents are not converted to a `Prodict` type, apparently.
    #
    # see also:
    #   https://github.com/ramazanpolat/prodict/issues/17
    #
    assert_eq2(result)


def test_scalpl(benchmark, my_data):
    result = benchmark(scalpl.Cut, my_data)
    # print(result)

    assert_eq5(result, subscript_list=True)


def test_simple_namespace(benchmark, my_data, parse_to_ns, ns_to_dict):
    result = benchmark(parse_to_ns, my_data)
    # print(result)

    assert_eq7(result, ns_to_dict)
