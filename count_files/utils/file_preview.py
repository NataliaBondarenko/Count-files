#!/usr/bin/env python3
# encoding: utf-8
import mimetypes
import locale
import subprocess
from pathlib import Path

from count_files.utils.file_handlers import get_file_extension
from count_files.settings import SUPPORTED_TYPES


def generic_text_preview(filepath: str, max_size: int) -> str:
    """Read the first characters of the file and return a string.

    First try to open the file with encoding='utf-8',
    if that fails (UnicodeDecodeError),
    then with the user's preferred encoding.

    :param filepath: a string containing the path to the file
    :param max_size: max number of characters to be read from file
    :return: a string with the text preview or error message
    """
    try:
        # try one of the most commonly used encodings
        # a string of ASCII text is also valid UTF-8 text
        with open(filepath, mode='r', encoding='utf-8') as f:
            return f.read(max_size).replace('\n', ' ')
    except Exception as e:
        if e.__class__ is UnicodeDecodeError:
            # try encoding used for text data, according to user preferences
            user_preferred_encoding = locale.getpreferredencoding(False)
            if user_preferred_encoding == 'UTF-8':
                return f"TEXT_PREVIEW_ERROR: {e.__class__.__name__}: {e}"
            else:
                try:
                    with open(filepath, mode='r', encoding=user_preferred_encoding) as f:
                        return f.read(max_size).replace('\n', ' ')
                except Exception as err:
                    return f"TEXT_PREVIEW_ERROR: {err.__class__.__name__}: {err}"
        else:
            return f"TEXT_PREVIEW_ERROR: {e.__class__.__name__}: {e}"


# TODO: build a better preview system for binaries
def generic_binary_preview(filepath: str, max_size: int) -> bytes or str:
    """ Read the first characters of the file and return a string

    :param filepath: a string containing the path to the file
    :param max_size: max number of characters to be read from file
    :return: a string with the text preview (without newline characters)
    """
    p = Path(filepath)  # TODO: do we need a Path() here? Path vs. built-in open()
    try:
        with p.open(mode='rb') as f:
            return f.read(max_size)
    except Exception as e:
        print("BINARY_PREVIEW_ERROR", e) # DEBUG
        return ""


def generate_preview(filepath: str, max_size: int = 390) -> str:
    """Generate a human readable text preview
    after checking if the extension is in the list of supported types.

    This function is used for all operating systems.

    For text files, the preview will be the first `max_size` characters.
    For other file types the preview is not implemented.
    :param filepath: full/path/to/file (with extension or without it)
    :param max_size:
    For CLI.
    The number of characters for viewing by default depends on the terminal width settings
    and can be changed with the -ps or -preview-size argument.
    :return: a string with the text preview (without newline characters).
    If the preview is not available for the file, it returns an information message.
    """
    extension = get_file_extension(filepath, case_sensitive=False).lower()

    if extension in SUPPORTED_TYPES['text']:
        excerpt = generic_text_preview(filepath, max_size)
        if excerpt:
            # return excerpt or error string
            return f"{excerpt}"
        else:
            return "[This file can be empty.]"
    else:
        # skip the extension if it is not supported
        return "[A preview of this file type is not yet implemented.]"


def generate_preview_with_file(filepath: str, max_size: int = 390) -> str:
    """Generate a human readable text preview
    after checking the file type with the Unix "file" command.

    This function is used in Linux, Mac OS and Windows
    (if the "file" program is installed
    and added to the PATH environment variable there).

    For text files, the preview will be the first `max_size` characters.
    For other file types the preview is not implemented.
    :param filepath: full/path/to/file (with extension or without it)
    :param max_size:
    For CLI.
    The number of characters for viewing by default depends on the terminal width settings
    and can be changed with the -ps or -preview-size argument.
    :return: a string with the text preview (without newline characters).
    If the preview is not available for the file, it returns an information message.
    """
    try:
        process_output = subprocess.run(
            ['file', filepath], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode('utf-8')
        # filepath: message\n
        message = process_output.split(': ')[1].strip('\n')
    except Exception as e:
        # OSError or CalledProcessError
        return f"TEXT_PREVIEW_ERROR: {e.__class__.__name__}: {e}"
    if 'cannot open' in message:
        # No such file or directory, or cannot read regular file
        return f"TEXT_PREVIEW_ERROR: {message}"
    elif 'empty' in message:
        return "[This file is empty.]"
    elif 'text' in message:
        excerpt = generic_text_preview(filepath, max_size)
        if excerpt:
            # return excerpt or error string
            return f"{excerpt}"
        else:
            return "[This file can be empty.]"
    else:
        # skip the extension if it is not supported
        # also: very short file (no magic)
        return f"[A preview of this file type is not yet implemented: {message}.]"
