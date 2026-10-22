"""
Models for test data
"""
from dataclasses import dataclass
from typing import List, Union

from dataclass_wizard import Alias


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
    camel_case: int = Alias('camelCase')
    snake_case: int = Alias('Snake_Case')
    pascal_case: int = Alias('PascalCase')
    spinal_case3: int = Alias('spinal-case3')
    hello: int = Alias('Hello, how\'s it going?')
    _3d: int = Alias('3D')
    for_: 'For' = Alias('for')
    some_random_key_here: Union[bool, str] = Alias('Some  r@ndom#$(*#@ Key##$# here   !!!')


@dataclass
class For:
    """
    For dataclass

    """
    infinity: List['Infinity'] = Alias('1nfinity')


@dataclass
class Infinity:
    """
    Infinity dataclass

    """
    and_: 'And' = Alias('and')


@dataclass
class And:
    """
    And dataclass

    """
    beyond: int = Alias('Beyond!')
