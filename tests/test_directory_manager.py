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
                "parent_id": "528c32f8-f5fc-4862-bbb8-3798c8e74a7c",
            },
            "8f04f1e9-922b-4ba5-bb44-fbc54035260a": {
                "name": "squash",
                "parent_id": "76ce2622-5886-4757-80a4-e2d5489202c1",
            },
        },
    }
    return dm


def test_add_folder(directory_manager):
    with patch.object(DirectoryManager, "_create_new_folder") as mock_create:
        directory_manager._add_folder("/fruits/apple")
        mock_create.assert_called_once_with(
            depth=1, folder_name="apple", parent_folder_name="fruits"
        )


def test_create_new_folder_root(directory_manager):
    with patch("uuid.uuid4", return_value="1234"):
        directory_manager._create_new_folder(depth=0, folder_name="fruits")
        assert "1234" in directory_manager.directory[0]
        assert directory_manager.directory[0]["1234"] == {
            "name": "fruits",
            "parent_id": None,
        }


def test_add_folder_invalid_path(directory_manager):
    directory_manager.directory = {}
    with patch("loguru.logger.warning") as mocked_warning:
        directory_manager._add_folder("/nonexistent/apple")
        mocked_warning.assert_any_call(
            "ERROR CREATING: nonexistent doesn't exist on parent level"
        )


def test_draw_directory(directory_manager):
    expected_output = (
        "foods\n" " grains\n" " fruits\n" "  fuji\n" " vegetables\n" "  squash\n"
    )

    with patch("loguru.logger.info") as mock_info:
        directory_manager._DirectoryManager__draw_directory()
        actual_output = "\n".join(call[0][0] for call in mock_info.call_args_list)
        assert actual_output.strip() == expected_output.strip()


def test_show_directory_empty():
    dm = DirectoryManager()

    with patch("loguru.logger.info") as mock_info:
        dm._show_directory()
        actual_output = "\n".join(call[0][0] for call in mock_info.call_args_list)
        assert actual_output.strip() == "LIST\nEMPTY DIRECTORY"


def test_show_directory_non_empty(directory_manager):
    expected_output = (
        "LIST\n"
        "foods\n"
        " grains\n"
        " fruits\n"
        "  fuji\n"
        " vegetables\n"
        "  squash\n"
    )

    with patch("loguru.logger.info") as mock_info:
        directory_manager._show_directory()
        actual_output = "\n".join(call[0][0] for call in mock_info.call_args_list)
        print(actual_output)
        assert actual_output.strip() == expected_output.strip()
