import sys
import traceback
from enum import Enum

from colored import attr, fg


class TealLevel(Enum):
    none = 0  # Prints no message, not even errors
    error = 1
    warning = 2
    info = 3  # Default
    verbose = 4
    debug = 5


class TealPrint:
    level: TealLevel = TealLevel.info

    @staticmethod
    def error(message: str, indent: int = 0, exit: bool = False, print_exception: bool = False):
        """Recommendation: Only use this when an error occurs and you have to exit the program
           Prints an error message in red, can quit and print an exception.
           Also prints a "Please report this and paste the above message"

        Args:
            message (str): The message to print
            indent (int): How many spaces to indent the message, indents by 4 spaces
            exit (bool): If the program should exit after printing the error
            print_exception (bool): Set to true to print an exception
        """
        TealPrint._print(message, indent, fg("red"), TealLevel.error)
        if print_exception:
            exception = traceback.format_exc()
            TealPrint._print(exception, 0, fg("red"), TealLevel.error)
        TealPrint._print("!!! Please report this and paste the above message !!!", 0, fg("red"), TealLevel.error, exit)
        if exit:
            sys.exit(1)

    @staticmethod
    def warning(message: str, indent: int = 0, exit: bool = False):
        """Prints an orange warning message message

        Args:
            message (str): The message to print
            indent (int): How many spaces to indent the message, indents by 4 spaces
            exit (bool): If the program should exit after printing the warning
        """
        TealPrint._print(message, indent, fg("dark_orange"), TealLevel.warning, exit)

    @staticmethod
    def info(message: str, indent: int = 0, color: str = ""):
        """Print a message if TealPrint.level has been set to debug/verbose/info

        Args:
            message (str): The message to print
            indent (int): How many spaces to indent the message, indents by 4 spaces
            color (LogColors): Optional color of the message
        """
        TealPrint._print(message, indent, color, TealLevel.info)

    @staticmethod
    def verbose(message: str, indent: int = 0, color: str = ""):
        """Prints a message if TealPrint.level has been set to debug/verbose

        Args:
            message (str): The message to print
            indent (int): How many spaces to indent the message, indents by 4 spaces
            color (LogColors): Optional color of the message
        """
        TealPrint._print(message, indent, color, TealLevel.verbose)

    @staticmethod
    def debug(message: str, indent: int = 0, color: str = ""):
        """Prints a message if the TealPrint.level has been set to debug

        Args:
            message (str): The message to print
            indent (int): How many spaces to indent the message, indents by 4 spaces
            color (LogColors): Optional color of the message
        """
        TealPrint._print(message, indent, color, TealLevel.debug)

    @staticmethod
    def _print(message: str, indent: int, color: str, level: TealLevel, exit: bool = False):
        if TealPrint.level.value >= level.value:
            if indent > 0:
                message = "".ljust(indent * 4) + message
            if len(color) > 0:
                message = f"{color}{message}{attr('reset')}"
            print(message)
        if exit:
            sys.exit(1)