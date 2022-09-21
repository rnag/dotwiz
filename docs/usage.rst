=====
Usage
=====

To use ``dotwiz`` in a project::

    from dotwiz import *

Default for Missing Keys
------------------------

The default behavior for :class:`DotWiz` or :class:`DotWizPlus` is
to |raise an AttributeError|_ if an attribute (key) doesn't exist::

    >>> from dotwiz import DotWiz
    >>> DotWiz(key='test').other_key
    Traceback (most recent call last):
      AttributeError: 'DotWiz' object has no attribute 'other_key'

The helper function :func:`set_default_for_missing_keys <dotwiz.set_default_for_missing_keys>` can be used
to return a *default* value for any missing attributes, as shown (or ``None`` if the argument is omitted).
This essentially implements a custom :meth:`__getattr__` on the public, exported classes.

.. code:: python3

    from dotwiz import DotWiz, DotWizPlus, set_default_for_missing_keys

    # if omitted, the default value is `None`
    set_default_for_missing_keys('test')

    dw = DotWiz(hello='world!')
    assert dw.hello == 'world!'
    assert dw.world == 'test'

    assert DotWizPlus().missing_key == 'test'

.. |raise an AttributeError| replace:: raise an :exc:`AttributeError`
.. _raise an AttributeError: https://github.com/rnag/dotwiz/issues/14

:class:`DotWizPlus`
-------------------

Simple usage with :class:`DotWizPlus <dotwiz.DotWizPlus>` to illustrate how keys with invalid characters
are made safe for attribute access:

.. code:: python3

    from dotwiz import DotWizPlus

    dw = DotWizPlus({
        'items': {
            'camelCase': 1,
            'TitleCase': 2,
            'Spinal-Case': 3,
            'To': {'1NFINITY': {'AND': {'Beyond  !! ': True}}},
            '1abc': 4,
            '42': 5,
            'Hello !@#&^+  W0rld   !!!': 'test',
        }
    })

    print(dw)
    # prints the following, on a single line:
    # >  ✪(items_=✪(camel_case=1, title_case=2, spinal_case=3,
    #               to=✪(_1nfinity=✪(and_=✪(beyond=True))),
    #                    _1abc=4, _42=5, hello_w0rld='test'))

    # confirm that we can access keys by dot (.) notation
    assert dw.items_.to._1nfinity.and_.beyond
    assert dw.items_._1abc == 4

    # the original keys can also be accessed like a normal `dict`, if needed
    assert dw['items']['To']['1NFINITY']['AND']['Beyond  !! ']

    print('to_dict() ->', dw.to_dict())
    # >  {'items': {'camelCase': 1, 'TitleCase': 2, ...}}

    print('to_attr_dict() ->', dw.to_attr_dict())
    # >  {'items_': {'camel_case': 1, 'title_case': 2, ...}}

    # get a JSON string representation with snake-cased keys, which strips out
    # underscores from the ends, such as for `and_` or `_42`.

    print('to_json(snake=True) ->', dw.to_json(snake=True))
    # >  {"items": {"camel_case": 1, "title_case": 2, ...}}

Complete Example
~~~~~~~~~~~~~~~~

Example with :func:`make_dot_wiz_plus <dotwiz.make_dot_wiz_plus>` to illustrate how :class:`DotWizPlus`
mutates keys with invalid characters to a safe, *snake-cased* format:

.. code:: python3

    from dotwiz import make_dot_wiz_plus

    dw = make_dot_wiz_plus(
        [
            # 1: reserved `keywords`
            ('class', 1), ('for', 1), ('lambda', 1), ('pass', 1),
            # 2: overwriting `dict` or `DotWizPlus` method names
            ('to_dict', 2), ('items', 2), ('keys', 2), ('copy', 2), ('values', 2),
            # 3: invalid identifiers
            ('99', 3), ('1abc', 3), ('x+y', 3),
            ('This  @!@# I!@#$%^&*()[]{};:"\'<,>.?/s    a test.', 3),
            ('Hello !@#&^+  W0rld   !!!', 3),
            # 4: special-cased keys
            ('Title Case', 4), ('SCREAMING_SNAKE_CASE', 4),
            ('camelCase', 4), ('PascalCase', 4), ('spinal-case', 4),
        ],
    )

    print(dw)
    # prints the following, on a single line:
    # >  ✪(class_=1, for_=1, lambda_=1, pass_=1,
    #      to_dict_=2, items_=2, keys_=2, copy_=2, values_=2,
    #      _99=3, _1abc=3, x_y=3, this_i_s_a_test=3, hello_w0rld=3,
    #      title_case=4, screaming_snake_case=4, camel_case=4, pascal_case=4, spinal_case=4)

    print(dw.to_dict())
    # >  {'class': 1, 'for': 1, ...}

    print(dw.to_attr_dict())
    # >  {'class_': 1, 'for_': 1, ...}

    # confirm that retrieving keys from the `DotWizPlus` instance by
    # attribute (dot) access works as expected.
    assert dw.class_ == dw.for_ == dw.lambda_ == dw.pass_ == 1
    assert dw.to_dict_ == dw.items_ == dw.keys_ == dw.copy_ == dw.values_ == 2
    assert dw._99 == dw._1abc == dw.x_y == dw.this_i_s_a_test == dw.hello_w0rld == 3
    assert dw.title_case == dw.screaming_snake_case == \
           dw.camel_case == dw.pascal_case == dw.spinal_case == 4


Type Hints and Auto Completion
------------------------------

For better code quality and to keep IDEs happy, it is possible to achieve auto-completion of key or attribute names,
as well as provide type hinting and auto-suggestion of ``str`` methods for example.

The simplest way to do it, is to extend from ``DotWiz`` or ``DotWiz+`` and use type annotations, as below.

    Note that this approach does **not** perform auto type conversion, such as ``str`` to ``int``.

.. code:: python3

    from typing import TYPE_CHECKING

    from dotwiz import DotWiz


    # create a simple alias.
    MyTypedWiz = DotWiz


    if TYPE_CHECKING:  # this only runs for static type checkers.

        class MyTypedWiz(DotWiz):
            # add attribute names and annotations for better type hinting!
            i: int
            b: bool
            nested: list['Nested']


        class Nested:
            s: str


    dw = MyTypedWiz(i=42, b=False, f=3.21, nested=[{'s': 'Hello, world!!'}])
    print(dw)
    # >  ✫(i=42, b=False, f=3.21, nested=[✫(s='Hello world!!')])

    # note that field (and method) auto-completion now works as expected!
    assert dw.nested[0].s.lower().rstrip('!') == 'hello, world'

    # we can still access non-declared fields, however auto-completion and type
    # hinting won't work as desired.
    assert dw.f == 3.21

    print('\nPrettified JSON string:')
    print(dw.to_json(indent=2))
    # prints:
    #   {
    #     "i": 42,
    #     "b": false,
    #     ...
    #   }
