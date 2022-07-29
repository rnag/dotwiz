from unittest.mock import MagicMock, mock_open

import pytest
from pytest_mock import MockerFixture


class FileMock(MagicMock):

    def __init__(self, mocker: MagicMock):
        super().__init__()

        self.__dict__ = mocker.__dict__

    @property
    def read_data(self):
        return self.side_effect

    @read_data.setter
    def read_data(self, mock_data: str):
        """set mock data to be returned when `open(...).read()` is called."""
        self.side_effect = mock_open(read_data=mock_data)


@pytest.fixture
def mock_file_open(mocker: MockerFixture) -> FileMock:
    return FileMock(mocker.patch('builtins.open'))
