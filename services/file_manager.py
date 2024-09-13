import os

from services import DirectoryManager


class FileManger:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.directory_manager = DirectoryManager()

    def _check_file_existence(self) -> bool:
        if not os.path.isfile(self.file_path):
            print(f"File not found: {self.file_path}")
            return False
        return True

    def _file_processing(self):
        with open(self.file_path, "r") as file:
            for line in file.readlines():
                self.directory_manager.command_execute(command=line.strip())

    def execute(self):
        file_existence = self._check_file_existence()
        if file_existence:
            self._file_processing()
