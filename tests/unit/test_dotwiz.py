"""Tests for `dotwiz` package."""

import pytest


from dotwiz import DotWiz, make_dot_wiz


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_make_dot_wiz():
    """Confirm correct functionality of `make_dot_wiz`"""
    dd = make_dot_wiz(a=1, b='two')

    assert repr(dd) == "DotWiz(a=1, b='two')"
    assert dd.a == 1
    assert dd.b == 'two'

    dd.b = [1, 2, 3]
    assert dd.b == [1, 2, 3]
