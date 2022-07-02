from types import SimpleNamespace

import pytest


@pytest.fixture
def parse_to_ns():
    """
    Return a helper function to parse a (nested) `dict` object
    and return a `SimpleNamespace` object.
    """

    def parse(d):
        ns = SimpleNamespace()

        for k, v in d.items():
            setattr(ns, k,
                    parse(v) if isinstance(v, dict)
                    else [parse(e) for e in v] if isinstance(v, list)
                    else v)

        return ns

    return parse


@pytest.fixture
def ns_to_dict():
    """
    Return a helper function to convert a `SimpleNamespace` object to
    a `dict`.
    """

    def to_dict(ns):
        """Recursively converts a `SimpleNamespace` object to a `dict`."""
        return {k: to_dict(v) if isinstance(v, SimpleNamespace)
                else [to_dict(e) for e in v] if isinstance(v, list)
                else v
                for k, v in vars(ns).items()}

    return to_dict
