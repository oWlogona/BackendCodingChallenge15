import uuid
from typing import Tuple

from loguru import logger


class DirectoryManager:
    """
    Manages a directory structure where folders can be created, listed, and organized in a hierarchical.
    """

    def __init__(self):
        """
        Initializes a new DirectoryManager with an empty directory structure.
        """
        self.directory = {}

    def __draw_directory(self):
        """
        Recursively prints the directory structure starting from the root level.

        This method helps visualize the directory structure in a hierarchical format,
        with indentation representing folder depth.
        """

        def print_folders(depth, parent_id=None, indent=""):
            """
            Helper function to recursively print folder names with proper indentation.

            Args:
                depth (int): The current depth level in the directory hierarchy.
                parent_id (str, optional): The parent folder ID to match for subfolders.
                indent (str): The current indentation string to format the output.
            """
            for item_id, item_info in sorted(self.directory.get(depth, {}).items()):
                if item_info["parent_id"] == parent_id:
                    logger.info(f"{indent}{item_info['name']}")
                    print_folders(depth + 1, item_id, indent + " ")

        print_folders(0)

    def _show_directory(self):
        """
        Prints the directory listing.

        Shows "LIST" followed by either the directory structure if it is not empty,
        or "EMPTY DIRECTORY" if the directory is empty.
        """
        logger.info("LIST")
        (
            logger.info("EMPTY DIRECTORY")
            if not self.directory
            else self.__draw_directory()
        )

    def _get_parent_folder_id(
        self, parent_folder_name: str, depth: int
    ) -> Tuple[str, bool]:
        """
        Retrieves the ID of a parent folder based on its name and depth level.

        Parameters:
        - parent_folder_name (str): The name of the parent folder to find.
        - depth (int): The depth level at which to search for the parent folder.

        Returns:
        - Tuple[str, bool]: A tuple where:
          - The first element is the ID of the parent folder if found, or an empty string if not found.
          - The second element is a boolean indicating whether the parent folder was found.
        """
        folders_name_parent_id = {
            val.get("name"): key for key, val in self.directory.get(depth, {}).items()
        }
        if folders_name_parent_id.get(parent_folder_name):
            return folders_name_parent_id.get(parent_folder_name), True
        return "", False

    def _create_new_folder(
        self, depth: int, folder_name: str, parent_folder_name: str = None
    ):
        """
        Creates a new folder at the specified depth in the directory structure.

        Parameters:
        - depth (int): The depth level where the new folder should be created.
        - folder_name (str): The name of the new folder.
        - parent_folder_name (str, optional): The name of the parent folder at the level above.
          If not provided, the new folder is created at the root level.

        If the depth is 0, the folder is created at the root level with no parent.
        For other depths, the method will check if the specified parent folder exists.
        If the parent folder exists, the new folder is added under it; otherwise, an error is printed.

        The method generates a unique ID for the new folder and updates the directory structure accordingly.
        """
        un_id = str(uuid.uuid4())
        if depth not in self.directory:
            self.directory[depth] = {}

        if depth == 0:
            self.directory[depth][un_id] = {"name": folder_name, "parent_id": None}
        else:
            parent_id, status = self._get_parent_folder_id(
                parent_folder_name=parent_folder_name, depth=depth - 1
            )
            if status:
                self.directory[depth][un_id] = {
                    "name": folder_name,
                    "parent_id": parent_id,
                }
            else:
                logger.warning(
                    f"ERROR CREATING: {parent_folder_name} doesn't exist on parent level"
                )

    def _add_folder(self, folder_path: str):
        """
        Adds a new folder to the directory structure based on the provided path.

        Args:
            folder_path (str): The path of the folder to be added, formatted as a string with folders separated by slashes ("/").

        This method parses the folder path to determine the folder's depth and parent folder, then creates the new folder
        accordingly. It prints a confirmation message once the folder is created.
        """
        folder_path_items = folder_path.strip("/").split("/")
        folder_depth = len(folder_path_items) - 1
        if folder_depth == 0:
            self._create_new_folder(
                depth=folder_depth, folder_name=folder_path_items[-1]
            )
        else:
            self._create_new_folder(
                depth=folder_depth,
                folder_name=folder_path_items[-1],
                parent_folder_name=folder_path_items[-2],
            )
        logger.info(f"CREATE {folder_path}")

    def __processing_child_folders(self, depth: int, offset: int, parent_id: str):
        """
        Processes and repositions child folders under a specified parent folder after a move operation.

        Args:
            depth (int): The current depth of the folder being processed.
            offset (int): The difference in depth between the original and new locations of the moved folder.
            parent_id (str): The ID of the parent folder whose children are being processed.

        Notes:
            - This method is used to adjust the depth of child folders after a folder has been moved.
            - It recursively updates the depth of each child folder based on the offset.
        """

        def processing_child(depth, parent_id, offset):
            for item_id, item_info in sorted(self.directory.get(depth, {}).items()):
                if item_info["parent_id"] == parent_id:
                    self.directory.get(depth).pop(item_id)
                    new_depth = depth - offset if offset > 0 else 2
                    self.directory[new_depth][item_id] = item_info
                    processing_child(depth + 1, item_id, offset)

        processing_child(depth=depth, parent_id=parent_id, offset=offset)

    def __move_folder(
        self, depth: int, new_depth: int, folder_name: str, new_folder_name: str
    ):
        """
        Moves a folder from its current location to a new location within the directory structure.

        Args:
            depth (int): The current depth of the folder to be moved.
            new_depth (int): The target depth where the folder should be moved.
            folder_name (str): The name of the folder to be moved.
            new_folder_name (str): The name of the target folder where the folder should be moved.

        Notes:
            - The method handles moving a folder by adjusting its position in the directory structure.
            - The movement involves updating the folder's parent ID and recursively processing child folders.
        """
        offset_cursor = 0

        parent_id, status = self._get_parent_folder_id(
            parent_folder_name=folder_name, depth=depth
        )
        if not status:
            logger.warning(f"ERROR MOVE: {folder_name} doesn't exist on level")
        transfer_data = self.directory.get(depth, {}).pop(parent_id)
        new_parent_id, new_status = self._get_parent_folder_id(
            parent_folder_name=new_folder_name, depth=new_depth
        )
        if not new_status:
            logger.warning(
                f"ERROR MOVE: {folder_name} to {new_folder_name} doesn't exist"
            )

        if depth > new_depth:
            offset_cursor = depth - (new_depth + 1)
            self.directory[depth - offset_cursor][parent_id] = {
                "name": transfer_data.get("name"),
                "parent_id": new_parent_id,
            }
            self.__processing_child_folders(
                depth + 1, offset=offset_cursor, parent_id=parent_id
            )

        if depth < new_depth:
            offset_cursor = new_depth - depth

        if depth == new_depth:
            depth = 1
            self.directory[depth - offset_cursor][parent_id] = {
                "name": transfer_data.get("name"),
                "parent_id": new_parent_id,
            }
            self.__processing_child_folders(
                depth=depth, offset=offset_cursor, parent_id=parent_id
            )

    def _move_folder(self, folder_path: str, new_folder_path: str):
        """
        Moves a folder from its current location to a new location in the directory structure.

        Args:
            folder_path (str): The current path of the folder to be moved. This should be a
                               hierarchical path like "/parent_folder/old_folder".
            new_folder_path (str): The new path where the folder should be moved. This should be a
                                   hierarchical path like "/new_parent_folder/new_folder".

        Notes:
            This method splits the folder paths into their respective components to determine
            the current depth and new depth of the folder being moved. It then calls the internal
            method to handle the actual moving process and prints a message confirming the move.
        """
        folder_path_items = folder_path.strip("/").split("/")
        folder_depth = len(folder_path_items) - 1
        new_folder_path_items = new_folder_path.strip("/").split("/")
        new_folder_depth = len(new_folder_path_items) - 1

        self.__move_folder(
            depth=folder_depth,
            folder_name=folder_path_items[-1],
            new_depth=new_folder_depth,
            new_folder_name=new_folder_path_items[-1],
        )
        logger.info(f"MOVE {folder_path} {new_folder_path}")

    def __delete_child_folders(self, depth: int, parent_id: str):
        """
        Recursively deletes all child folders under a specified parent folder.

        Args:
            depth (int): The current depth level in the directory hierarchy.
            parent_id (str): The ID of the parent folder whose child folders are to be deleted.

        Notes:
            This method starts at the given depth and deletes all folders that have the specified
            parent_id as their parent. It then recursively processes all subfolders at the next depth level.
        """

        def delete_child(depth, parent_id):
            """
            Helper function to recursively delete child folders.

            Args:
                depth (int): The current depth level in the directory hierarchy.
                parent_id (str): The ID of the parent folder whose child folders are being deleted.
            """
            for item_id, item_info in sorted(self.directory.get(depth, {}).items()):
                if item_info["parent_id"] == parent_id:
                    self.directory.get(depth).pop(item_id)
                    delete_child(depth + 1, item_id)

        delete_child(depth=depth, parent_id=parent_id)

    def _delete_folder(self, folder_path: str):
        """
        Deletes a folder and its subfolders from the directory structure.

        Args:
            folder_path (str): The path of the folder to delete. This should be a
                               hierarchical path like "/parent_folder/child_folder".

        Prints:
            An error message if the folder does not exist at the specified depth.

        Notes:
            This method assumes that the folder to be deleted is identified by its path,
            and it recursively deletes all subfolders within the specified folder.
        """
        logger.info(f"DELETE {folder_path}")
        folder_path_items = folder_path.strip("/").split("/")
        folder_depth = len(folder_path_items) - 1
        parent_id, status = self._get_parent_folder_id(
            parent_folder_name=folder_path_items[-1], depth=folder_depth
        )
        if not status:
            logger.warning(f"Cannot delete: {folder_path} doesn't exist on level")
        else:
            self.directory.get(folder_depth).pop(parent_id)
            self.__delete_child_folders(depth=folder_depth + 1, parent_id=parent_id)

    def _command_line_parser(self, command_line: str):
        """
        Parses and executes a command from a given file line string.

        The command line string should be in the format:
        "COMMAND [ARG1] [ARG2]"

        Where:
        - COMMAND is one of "CREATE", "LIST", "MOVE", or "DELETE".
        - ARG1 and ARG2 are arguments depending on the command.

        Args:
            command_line (str): The command line string to parse and execute.

        Actions:
            - If the command is "CREATE", calls `_add_folder` with `ARG1` as the folder path.
            - If the command is "LIST", calls `_show_directory` to display the directory.
            - If the command is "MOVE", calls `_move_folder` with `ARG1` as the folder path
              and `ARG2` as the new folder path.
            - If the command is "DELETE", calls `_delete_folder` with `ARG1` as the folder path.
        """
        parts = command_line.split(" ", 2)
        command, folder_path, new_folder_path = (parts + [None, None])[:3]
        if command == "CREATE":
            self._add_folder(folder_path=folder_path)
        if command == "LIST":
            self._show_directory()
        if command == "MOVE":
            self._move_folder(folder_path=folder_path, new_folder_path=new_folder_path)
        if command == "DELETE":
            self._delete_folder(folder_path=folder_path)

    def command_execute(self, command: str):
        """
        Executes a given command string by parsing and processing it.

        This method parses the command string and delegates the execution
        to the appropriate method based on the parsed command.

        Args:
            command (str): The command string to parse and execute.
                           Expected format: "COMMAND [ARG1] [ARG2]"

        Example:
            command_execute("CREATE /path/to/folder")
            command_execute("LIST")
            command_execute("MOVE /path/to/old_folder /path/to/new_folder")
            command_execute("DELETE /path/to/folder")
        """
        self._command_line_parser(command)
