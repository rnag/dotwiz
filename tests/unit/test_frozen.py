import pytest

from dotwiz.frozen import NotDotWiz, FrozenDotWizError


def test_not_dot_wiz_is_immutable():
    """
    Test that :class:`NotDotWiz` is immutable, i.e. it cannot be
    modified (easily).
    """
    dw = NotDotWiz()

    with pytest.raises(FrozenDotWizError):
        dw.k2 = 'value'

    with pytest.raises(FrozenDotWizError):
        dw['k3'] = 'value'

    with pytest.raises(FrozenDotWizError):
        dw.update(k4='value')

    with pytest.raises(FrozenDotWizError):
        dw.setdefault('k5', 'value')


def test_not_dot_wiz_bool():
    dw = NotDotWiz()
    assert not dw
