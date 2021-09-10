import sys
import traceback
from io import StringIO
from threading import Lock

from colored import attr, fg

from . import TealConfig, TealLevel


class TealPrintBuffer:
    _mutex = Lock()
    _ascii: bool = False

    def __init__(self) -> None:
        self.buffer = StringIO()

    def error(
        self,
        message: str,
        indent: int = 0,
        exit: bool = False,
        print_exception: bool = False,
        print_report_this: bool = False,
    ) -> None:
        """Recommendation: Only use this when an error occurs and you have to exit the program.
           Add an error message in red to the buffer. Can print the exception.
           If exit=True, it flushes all messages before exiting.
           Optionally prints a "Please report this and paste the above message"
           Call flush() to print the messages.

        Args:
            message (str): The message to print
            indent (int): How many spaces to indent the message, indents by 4 spaces
            exit (bool): If the program should exit after printing the error. Also flushes messages
            print_exception (bool): Set to true to print an exception
            print_report_this (bool): Set to true to add an "Please report this..." message at the end
        """
        self._add_to_buffer_on_level(message, indent, fg("red"), TealLevel.error)
        if print_exception:
            exception = traceback.format_exc()
            self._add_to_buffer_on_level(exception, 0, fg("red"), TealLevel.error)
        if print_report_this:
            self._add_to_buffer_on_level(
                "!!! Please report this and paste the above message !!!", 0, fg("red"), TealLevel.error
            )
        if exit:
            self.flush()
            sys.exit(1)

    def warning(self, message: str, indent: int = 0, exit: bool = False) -> None:
        """Add an orange warning message to the buffer.
           If exit=True, it flushes all messages before exiting.
           Call flush() to print the messages.

        Args:
            message (str): The message to print
            indent (int): How many spaces to indent the message, indents by 4 spaces
            exit (bool): If the program should exit after printing the warning. Also flushes messages
        """
        self._add_to_buffer_on_level(message, indent, fg("dark_orange"), TealLevel.warning, exit)

    def info(self, message: str, indent: int = 0, color: str = "") -> None:
        """Add a message to the buffer if TealConfig.level has been set to debug/verbose/info.
           Call flush() to print the messages.

        Args:
            message (str): The message to print
            indent (int): How many spaces to indent the message, indents by 4 spaces
            color (str): Optional color of the message
        """
        self._add_to_buffer_on_level(message, indent, color, TealLevel.info)

    def verbose(self, message: str, indent: int = 0, color: str = "") -> None:
        """Add a message to the buffer if TealConfig.level has been set to debug/verbose.
           Call flush() to print the messages.

        Args:
            message (str): The message to print
            indent (int): How many spaces to indent the message, indents by 4 spaces
            color (str): Optional color of the message
        """
        self._add_to_buffer_on_level(message, indent, color, TealLevel.verbose)

    def debug(self, message: str, indent: int = 0, color: str = "") -> None:
        """Add a message to the buffer if the TealConfig.level has been set to debug.
           Call flush() to print the messages.

        Args:
            message (str): The message to print
            indent (int): How many spaces to indent the message, indents by 4 spaces
            color (str): Optional color of the message
        """
        self._add_to_buffer_on_level(message, indent, color, TealLevel.debug)

    def _add_to_buffer_on_level(
        self,
        message: str,
        indent: int,
        color: str,
        level: TealLevel,
        exit: bool = False,
    ) -> None:
        """Prints the message if the level is equal or lower to the specified"""
        if TealConfig.level.value >= level.value:
            try:
                if indent > 0:
                    message = "".ljust(indent * TealConfig.indent_by, TealConfig.indent_char) + message
                if len(color) > 0:
                    message = f"{color}{message}{attr('reset')}"

                if TealPrintBuffer._ascii:
                    message = message.encode("utf-8", "ignore").decode("ascii", "ignore")

                self._add_to_buffer(message)
                if exit:
                    self.flush()
                    sys.exit(1)
            except UnicodeEncodeError:
                # Some consoles can't use utf-8, encode into ascii instead, and use that
                # in the future
                TealPrintBuffer._ascii = True
                self._add_to_buffer_on_level(message, indent, color, level, exit)

    def _add_to_buffer(self, message: str) -> None:
        """Mostly used for mocking purposes"""
        self.buffer.write(message + "\n")

    def flush(self) -> None:
        """Prints the messages in the buffer"""
        self.buffer.seek(0)

        # Make sure we only print one message at a time
        TealPrintBuffer._mutex.acquire()
        try:
            print(self.buffer.read(), flush=True)
        finally:
            TealPrintBuffer._mutex.release()

        self.buffer = StringIO()
