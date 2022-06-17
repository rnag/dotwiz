"""
Models for test data
"""
from dataclasses import dataclass
from typing import List, Union

from dataclass_wizard import json_field


@dataclass
class MyClass:
    a: int
    b: int
    c: 'Nested1'


@dataclass
class Nested1:
    aa: int
    bb: List['Nested2']


@dataclass
class Nested2:
    x: int


@dataclass
class MyClassSpecialCased:
    """
    MyClassSpecialCased dataclass

    """
    camel_case: int
    snake_case: int
    pascal_case: int
    spinal_case3: int
    hello: int = json_field('Hello, how\'s it going?')
    _3d: int = json_field('3D')
    for_: 'For' = json_field('for')
    some_random_key_here: Union[bool, str] = json_field('Some  r@ndom#$(*#@ Key##$# here   !!!')


@dataclass
class For:
    """
    For dataclass

    """
    infinity: List['Infinity'] = json_field('1nfinity')


@dataclass
class Infinity:
    """
    Infinity dataclass

    """
    and_: 'And' = json_field('and')


@dataclass
class And:
    """
    And dataclass

    """
    beyond: int = json_field('Beyond!')
