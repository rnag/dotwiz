"""Reusable test utilities and fixtures."""
import pytest

from dotwiz import DotWiz, DotWizPlus


class CleanupGetAttr:

    def teardown_method(self):
        """Runs at the end of each test method in the class.

        Remove :meth:`__getattr__` from all publicly exposed classes.

        For more info, see:
            * https://docs.pytest.org/en/latest/how-to/fixtures.html#teardown-cleanup-aka-fixture-finalization
            * https://docs.pytest.org/en/latest/how-to/xunit_setup.html#method-and-function-level-setup-teardown

        """
        del DotWiz.__getattr__
        del DotWizPlus.__getattr__
