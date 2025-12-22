import os


class FileManager:

    @staticmethod
    def checkFile(file_path):
        """Verify if a file exists."""
        return os.path.isfile(file_path)

    @staticmethod
    def extractFileName(file_path):
        """Returns only the name of the file by its complete path."""
        # return os.path.basename(urlparse(file_path).path)
        return os.path.basename(file_path)

    @staticmethod
    def updatingFile(file_path, content):
        """Overwrite the content of an existing file."""
        try:
            with open(file_path, "w") as f:
                f.write(content)

        except FileExistsError as error:
            print(f"Error when trying to update file: {error}.")

    @staticmethod
    def read(file_path):
        """Read the content of a file and returns it as string. In case of error, returns None"""
        try:
            with open(file_path, "r") as f:
                return f.read()
        except FileNotFoundError:
            print(f"Error: The file '{file_path}' was not found.")
            return None
        except FileExistsError as error:
            print(f"Error: file does not exist: {error}.")
            return None
        except Exception as error:
            print(f"Error: Not possible to read the file: {error}")
            return None

    @staticmethod
    def append(file_path, content):
        """Adds content to the end of a file."""
        try:
            with open(file_path, "w") as f:
                f.write(content)
        except Exception as error:
            print(f"Error when trying to add content to file: {error}")
