import pytest

from dotwiz.frozen import FrozenDotWiz, FrozenDotWizError


def test_frozen_dot_wiz_is_immutable():
    """
    Test that :class:`FrozenDotWiz` is immutable, i.e. it cannot be
    modified (easily).
    """
    dw = FrozenDotWiz(k1='value')

    with pytest.raises(FrozenDotWizError):
        dw.k2 = 'value'

    with pytest.raises(FrozenDotWizError):
        dw['k3'] = 'value'

    with pytest.raises(FrozenDotWizError):
        dw.update(k4='value')

    with pytest.raises(FrozenDotWizError):
        dw.setdefault('k5', 'value')

    assert dw.to_dict() == {'k1': 'value'}
