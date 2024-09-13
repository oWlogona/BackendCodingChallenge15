import os

from services import DirectoryManager


class FileManger:
    """
    A class to manage file operations and directory updates based on file contents.

    Attributes:
        file_path (str): The path to the file to be processed.
        directory_manager (DirectoryManager): An instance of DirectoryManager for managing directory operations.
    """

    def __init__(self, file_path: str):
        """
        Initializes the FileManger with the path to the file.

        Args:
            file_path (str): The path to the file to be processed.
        """
        self.file_path = file_path
        self.directory_manager = DirectoryManager()

    def _check_file_existence(self) -> bool:
        """
        Checks if the file at the specified file path exists.

        Returns:
            bool: True if the file exists, False otherwise. If the file does not exist, a message is printed.
        """
        if not os.path.isfile(self.file_path):
            print(f"File not found: {self.file_path}")
            return False
        return True

    def _file_processing(self):
        """
        Processes the file at the specified file path. Reads each line from the file and executes
        directory commands using the DirectoryManager instance.

        Assumes that each line in the file represents a command to be executed.
        """
        with open(self.file_path, "r") as file:
            for line in file.readlines():
                self.directory_manager.command_execute(command=line.strip())

    def execute(self):
        """
        Executes the file processing workflow.

        First, it checks if the file exists. If the file exists, it proceeds to process
        the file and update the directory.
        """
        file_existence = self._check_file_existence()
        if file_existence:
            self._file_processing()
