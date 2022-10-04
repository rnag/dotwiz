"""Reusable test utilities and fixtures."""
try:
    from functools import cached_property
except ImportError:  # Python <= 3.7
    # noinspection PyUnresolvedReferences, PyPackageRequirements
    from backports.cached_property import cached_property

from unittest.mock import MagicMock, mock_open

import pytest
from pytest_mock import MockerFixture

from dotwiz import DotWiz, DotWizPlus


class FileMock(MagicMock):

    def __init__(self, mocker: MagicMock = None, **kwargs):
        super().__init__(**kwargs)

        if mocker:
            self.__dict__ = mocker.__dict__
            # configure mock object to replace the use of open(...)
            # note: this is useful in scenarios where data is written out
            _ = mock_open(mock=self)

    @property
    def read_data(self):
        return self.side_effect

    @read_data.setter
    def read_data(self, mock_data: str):
        """set mock data to be returned when `open(...).read()` is called."""
        self.side_effect = mock_open(read_data=mock_data)

    @cached_property
    def write_calls(self):
        """a list of calls made to `open().write(...)`"""
        handle = self.return_value
        write: MagicMock = handle.write
        return write.call_args_list

    @property
    def write_lines(self) -> str:
        """a list of written lines (as a string)"""
        return ''.join([c[0][0] for c in self.write_calls])


@pytest.fixture
def mock_file_open(mocker: MockerFixture) -> FileMock:
    return FileMock(mocker.patch('builtins.open'))


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
