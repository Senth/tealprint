import sys
import traceback

from colored import attr, fg

from .teallevel import TealLevel


class TealPrint:
    level: TealLevel = TealLevel.info
    _ascii: bool = False

    @staticmethod
    def error(
        message: str,
        indent: int = 0,
        exit: bool = False,
        print_exception: bool = False,
        print_report_this: bool = False,
    ):
        """Recommendation: Only use this when an error occurs and you have to exit the program
           Prints an error message in red, can quit and print an exception.
           Also prints a "Please report this and paste the above message"

        Args:
            message (str): The message to print
            indent (int): How many spaces to indent the message, indents by 4 spaces
            exit (bool): If the program should exit after printing the error
            print_exception (bool): Set to true to print an exception
            print_report_this (bool): Set to true to add an "Please report this..." message at the end
        """
        TealPrint._print_on_level(message, indent, fg("red"), TealLevel.error)
        if print_exception:
            exception = traceback.format_exc()
            TealPrint._print_on_level(exception, 0, fg("red"), TealLevel.error)
        if print_report_this:
            TealPrint._print_on_level(
                "!!! Please report this and paste the above message !!!", 0, fg("red"), TealLevel.error
            )
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
        TealPrint._print_on_level(message, indent, fg("dark_orange"), TealLevel.warning, exit)

    @staticmethod
    def info(message: str, indent: int = 0, color: str = ""):
        """Print a message if TealPrint.level has been set to debug/verbose/info

        Args:
            message (str): The message to print
            indent (int): How many spaces to indent the message, indents by 4 spaces
            color (str): Optional color of the message
        """
        TealPrint._print_on_level(message, indent, color, TealLevel.info)

    @staticmethod
    def verbose(message: str, indent: int = 0, color: str = ""):
        """Prints a message if TealPrint.level has been set to debug/verbose

        Args:
            message (str): The message to print
            indent (int): How many spaces to indent the message, indents by 4 spaces
            color (str): Optional color of the message
        """
        TealPrint._print_on_level(message, indent, color, TealLevel.verbose)

    @staticmethod
    def debug(message: str, indent: int = 0, color: str = ""):
        """Prints a message if the TealPrint.level has been set to debug

        Args:
            message (str): The message to print
            indent (int): How many spaces to indent the message, indents by 4 spaces
            color (str): Optional color of the message
        """
        TealPrint._print_on_level(message, indent, color, TealLevel.debug)

    @staticmethod
    def _print_on_level(message: str, indent: int, color: str, level: TealLevel, exit: bool = False):
        """Prints the message if the level is equal or lower to the specified"""
        if TealPrint.level.value >= level.value:
            try:
                if indent > 0:
                    message = "".ljust(indent * 4) + message
                if len(color) > 0:
                    message = f"{color}{message}{attr('reset')}"

                if TealPrint._ascii:
                    message = message.encode("utf-8", "ignore").decode("ascii", "ignore")

                TealPrint._print(message)
                if exit:
                    sys.exit(1)
            except UnicodeEncodeError:
                # Some consoles can't use utf-8, encode into ascii instead, and use that
                # in the future
                TealPrint._ascii = True
                TealPrint._print_on_level(message, indent, color, level, exit)

    @staticmethod
    def _print(message):
        """Mostly used for mocking purposes"""
        print(message)
