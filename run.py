import argparse

from services import FileManger

if __name__ == "__main__":
    """
    Main entry point of the script.

    Parses command-line arguments to get the file path, initializes a FileManager
    instance with the given file path, and executes the file processing.
    """
    parser = argparse.ArgumentParser(description="Process a file.")
    parser.add_argument("file_path", type=str, help="Path to the file to process")
    args = parser.parse_args()

    file_manager = FileManger(file_path=args.file_path)
    file_manager.execute()
