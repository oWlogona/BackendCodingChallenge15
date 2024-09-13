import argparse
import os
import uuid
from collections import defaultdict
from typing import Tuple


class DirectoryManager:
    def __init__(self):
        self.directory = {}

    def __draw_directory(self):
        def print_folders(depth, parent_id=None, indent=""):
            for item_id, item_info in sorted(self.directory.get(depth, {}).items()):
                if item_info["parent_id"] == parent_id:
                    print(f"{indent}{item_info['name']}")
                    print_folders(depth + 1, item_id, indent + " ")

        print_folders(0)

    def _show_directory(self):
        print("LIST")
        print("EMPTY DIRECTORY") if not self.directory else self.__draw_directory()

    def _get_parent_folder_id(self, parent_folder_name: str, depth: int) -> Tuple[str, bool]:
        folders_name_parent_id = {val.get("name"): key for key, val in self.directory.get(depth, {}).items()}
        if folders_name_parent_id.get(parent_folder_name):
            return folders_name_parent_id.get(parent_folder_name), True
        return "", False

    def _create_new_folder(self, depth: int, folder_name: str, parent_folder_name: str = None):
        un_id = str(uuid.uuid4())
        if depth not in self.directory:
            self.directory[depth] = {}

        if depth == 0:
            self.directory[depth][un_id] = {"name": folder_name, "parent_id": None}
        else:
            parent_id, status = self._get_parent_folder_id(parent_folder_name=parent_folder_name, depth=depth - 1)
            if status:
                self.directory[depth][un_id] = {"name": folder_name, "parent_id": parent_id}
            else:
                print(f"ERROR CREATING: {parent_folder_name} doesn't exist on parent level")

    def _add_folder(self, folder_path: str):
        folder_path_items = folder_path.strip('/').split('/')
        folder_depth = len(folder_path_items) - 1
        if folder_depth == 0:
            self._create_new_folder(depth=folder_depth, folder_name=folder_path_items[-1])
        else:
            self._create_new_folder(depth=folder_depth, folder_name=folder_path_items[-1],
                                    parent_folder_name=folder_path_items[-2])
        print(f"CREATE {folder_path}")

    def __processing_child_folders(self, depth: int, offset:int, parent_id: str):
        def processing_child(depth, parent_id, offset):
            for item_id, item_info in sorted(self.directory.get(depth, {}).items()):
                if item_info["parent_id"] == parent_id:
                    self.directory.get(depth).pop(item_id)
                    new_depth = depth-offset if offset > 0 else 2
                    self.directory[new_depth][item_id] = item_info
                    print("depth: ", depth, item_info, new_depth)
                    processing_child(depth + 1, item_id, offset)

        processing_child(depth=depth, parent_id=parent_id, offset=offset)


    def __move_folder(self, depth: int, new_depth: int, folder_name: str, new_folder_name: str):
        offset_cursor = 0

        parent_id, status = self._get_parent_folder_id(parent_folder_name=folder_name, depth=depth)
        if not status:
            print(f"ERROR MOVE: {folder_name} doesn't exist on level")
        transfer_data = self.directory.get(depth, {}).pop(parent_id)
        new_parent_id, new_status = self._get_parent_folder_id(parent_folder_name=new_folder_name, depth=new_depth)
        if not new_status:
            print(f"ERROR MOVE: {folder_name} to {new_folder_name} doesn't exist")

        if depth > new_depth:
            offset_cursor = depth - (new_depth+1)
            self.directory[depth - offset_cursor][parent_id] = {"name": transfer_data.get("name"),
                                                                "parent_id": new_parent_id}
            self.__processing_child_folders(depth + 1, offset=offset_cursor, parent_id=parent_id)

        if depth < new_depth:
            offset_cursor = new_depth - depth

        if depth == new_depth:
            depth = 1
            self.directory[depth - offset_cursor][parent_id] = {"name": transfer_data.get("name"),
                                                                "parent_id": new_parent_id}
            self.__processing_child_folders(depth=depth, offset=offset_cursor, parent_id=parent_id)


    def _move_folder(self, folder_path: str, new_folder_path: str):
        folder_path_items = folder_path.strip('/').split('/')
        folder_depth = len(folder_path_items) - 1
        new_folder_path_items = new_folder_path.strip('/').split('/')
        new_folder_depth = len(new_folder_path_items) - 1

        self.__move_folder(depth=folder_depth, folder_name=folder_path_items[-1], new_depth=new_folder_depth,
                           new_folder_name=new_folder_path_items[-1])
        print(f"MOVE {folder_path} {new_folder_path}")

    def __delete_child_folders(self, depth: int, parent_id: str):
        def delete_child(depth, parent_id):
            for item_id, item_info in sorted(self.directory.get(depth, {}).items()):
                if item_info["parent_id"] == parent_id:
                    self.directory.get(depth).pop(item_id)
                    delete_child(depth + 1, item_id)

        delete_child(depth=depth, parent_id=parent_id)

    def _delete_folder(self, folder_path: str):
        folder_path_items = folder_path.strip('/').split('/')
        folder_depth = len(folder_path_items) - 1
        parent_id, status = self._get_parent_folder_id(parent_folder_name=folder_path_items[-1], depth=folder_depth)
        if not status:
            print(f"Cannot delete: {folder_path} doesn't exist on level")
        else:
            self.directory.get(folder_depth).pop(parent_id)
            self.__delete_child_folders(depth=folder_depth+1, parent_id=parent_id)

    def _command_line_parser(self, command_line: str):
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

        print('*'*10)

    def command_execute(self, command: str):
        self._command_line_parser(command)


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
        with open(self.file_path, 'r') as file:
            for line in file.readlines():
                self.directory_manager.command_execute(command=line.strip())

    def execute(self):
        file_existence = self._check_file_existence()
        if file_existence:
            self._file_processing()


commands_list = ["CREATE", "MOVE", "DELETE", "LIST"]

if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description="Process a file.")
    # parser.add_argument('file_path', type=str, help="Path to the file to process")
    # args = parser.parse_args()

    file_manager = FileManger(file_path="inst2.txt")
    file_manager.execute()
