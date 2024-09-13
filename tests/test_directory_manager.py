from io import StringIO
from unittest.mock import patch

import pytest

from services import DirectoryManager


@pytest.fixture
def directory_manager():
    dm = DirectoryManager()
    dm.directory = {
        0: {
            "b896a298-5e4c-4841-8c88-d95dfb31b400": {"name": "foods", "parent_id": None}
        },
        1: {
            "4146aee1-065b-47b5-9acf-c5eaedd712bd": {
                "name": "grains",
                "parent_id": "b896a298-5e4c-4841-8c88-d95dfb31b400",
            },
            "528c32f8-f5fc-4862-bbb8-3798c8e74a7c": {
                "name": "fruits",
                "parent_id": "b896a298-5e4c-4841-8c88-d95dfb31b400",
            },
            "76ce2622-5886-4757-80a4-e2d5489202c1": {
                "name": "vegetables",
                "parent_id": "b896a298-5e4c-4841-8c88-d95dfb31b400",
            },
        },
        2: {
            "de54de84-83e0-48ae-b3ac-ecd760229c81": {
                "name": "fuji",
                "parent_id": "fe9fe360-9318-40ca-8b2e-11affd859939",
            },
            "8f04f1e9-922b-4ba5-bb44-fbc54035260a": {
                "name": "squash",
                "parent_id": "76ce2622-5886-4757-80a4-e2d5489202c1",
            },
        },
    }
    return dm


def test_draw_directory(directory_manager):
    expected_output = "foods\n" " grains\n" " fruits\n" " vegetables\n" "  squash\n"

    with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
        directory_manager._DirectoryManager__draw_directory()
        assert mock_stdout.getvalue() == expected_output


def test_show_directory_empty():
    dm = DirectoryManager()

    with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
        dm._show_directory()
        assert mock_stdout.getvalue().strip() == "LIST\nEMPTY DIRECTORY"


def test_show_directory_non_empty(directory_manager):
    expected_output = (
        "LIST\n" "foods\n" " grains\n" " fruits\n" " vegetables\n" "  squash\n"
    )

    with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
        directory_manager._show_directory()
        assert mock_stdout.getvalue() == expected_output
