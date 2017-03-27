import io

from typing import Union, IO, Any, Optional

class OpenResult(object):

    def __init__(self) -> None:
        self.contents = None # type: Optional[str]
        self.error_message = ""


class FileContext(object):

    def __init__(self, path: str, mode: str) -> None:
        self.path = path
        self.mode = mode
        self.file = None # type: Optional[IO[Any]]

    def __enter__(self) -> OpenResult:
        try:
            with open(self.path, self.mode) as open_file:
                self.file = open_file
                result = OpenResult()
                result.contents = open_file.read()
                return result

        except OSError as e:
            result = OpenResult()
            result.error_message = e.strerror
            return result

    def __exit__(self, *args):
        if self.file != None:
            self.file.close()

def open_file(path: str, mode: str) -> FileContext:
    return FileContext(path, mode)
