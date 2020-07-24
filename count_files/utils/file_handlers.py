#!/usr/bin/env python3
# encoding: utf-8
import os
import sys
import subprocess
from itertools import chain
from typing import List, Tuple, Dict

from count_files.settings import SUPPORTED_TYPES, BUG_REPORT_URL


def get_file_extension(filepath: str, case_sensitive: bool = False) -> str:
    """Extract only the file extension from a given path.

    Behavior:
    select2.3805311d5fc1.css.gz -> gz, .gitignore -> '.'
    Pipfile -> '.', .hidden_file.txt -> txt
    Used in platforms.py and file_preview.py
    :param filepath: full/path/to/file or filename
    :param case_sensitive: False -> ignore case in extensions,
    True -> distinguish case variations in extensions
    :return: extension name (txt, py) or '.' (for files without extension).
    If case_sensitive==False, return in uppercase.
    """
    extension = os.path.splitext(filepath)[1][1:]
    if extension:
        if case_sensitive:
            return extension
        else:
            return extension.upper()
    else:
        return '.'


def is_supported_filetype(extension: str) -> bool:
    """Return a True if the given file extension has a supported file preview.

    :param extension: extension name (txt, py), '.'(without extension) or '..' (all extensions)
    :return: True if we have a preview procedure for the given file type, False otherwise.
    """
    return extension in list(chain.from_iterable(SUPPORTED_TYPES.values()))


def group_ext_by_type(data: List[Tuple[str, int]],
                      ext_and_group: Dict[str, str]) -> Dict[str, List[Tuple[str, int]]]:
    """Group file extensions by type.

    Default ext_and_group:
    archives, audio, audio/video, data, documents, executables, fonts, images,
    Python related extensions, videos, and other files.
    User-defined ext_and_group:
    may be created from configuration file.
    Initial storage: dict with items like {'documents': [], 'images': [], ...}
    key - group name, value - empty list.
    'other': reserved key.
    :param data: list with items like [('png', 8), ('txt', 25), ...]
    :param ext_and_group: dict with items like {'png': 'image', 'txt': documents, ...}
    :return: sorted dict with items like {'documents': [('txt', 25), ...], 'images': [('png', 8), ...], ...}
    """
    # storage: Dict[str, list]
    # local scope important
    storage = dict.fromkeys(sorted(set(ext_and_group.values())), [])
    other = []
    for (ext, freq) in data:
        item_type = ext_and_group.get(ext.lower(), 'other')
        if item_type == 'other':
            other.append((ext, freq))
        else:
            if storage.get(item_type):
                storage[item_type].append((ext, freq))
            else:
                storage[item_type] = [(ext, freq)]
    if other:
        storage.update({'other': other})
    return storage


def is_file_utility_available(file_path: str, expected_result: str) -> [bool, str]:
    """Check if the Unix "file" command is available and works as expected.

    The "file" command is a standard program on Unix and Unix-like OS
    for guessing the type of data contained in a file.

    This program can be used on Windows.
    For example, if the user installed it along with Git (https://git-scm.com)
    and added it to the PATH environment variable.
    It can usually be located as C:\\Program Files\\Git\\usr\\bin\\file.exe

    :param file_path: test path must exist
    :param expected_result: expected standard output of Unix "file" command for a path
    :return: True, None or False, error message
    """
    try:
        file_help_text = subprocess.run(
            ['file', '--help'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode('utf-8')
        if 'Determine type of FILEs.' not in file_help_text:
            msg = '\nAn error occurred while checking the "file" command.\n' \
                  'Calling the "file" command with the "--help" option returned unexpected results.\n' \
                  'Make sure you are applying the correct "file" program to your files.\n'
            return False, msg
        output = subprocess.run(
            ['file', file_path], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode('utf-8')
        if output == expected_result:
            return True, None
        else:
            msg = '\nAn error occurred while checking the "file" command.\n' \
                  'Applying the "file" command to the test path returned unexpected results.\n' \
                  'Make sure you are applying the correct "file" program to your files.\n'
            return False, msg
    except Exception as e:
        # most common exception raised is OSError, FileNotFoundError: [Errno 2] No such file or directory: ...
        # or  CalledProcessError: Command ... returned non-zero exit status 1 (unknown option, etc.)
        msg = '\nAn error occurred while checking the "file" command.\n' \
              f'{e.__class__.__name__}: {e}\n' \
              'Make sure you are applying the correct "file" program to your files.\n' \
              f'You can also report a problem at {BUG_REPORT_URL}\n'
        return False, msg


def check_shell_command() -> [bool, str]:
    """Checking if we can use the Unix "file" command
    to determine the file type for the preview.

    In CLI, the path to the "count_files/utils/test" directory is used
    to check the availability of the "file" program.

    :return: True, None or False, error message
    if False use default list of text extensions.
    """
    if not any([sys.platform.startswith('win'),
                sys.platform.startswith('linux'),
                sys.platform.startswith('darwin')]):
        msg = '\nThe use of "-sc file" or "--shell-command file" on your operating system ' \
              'is not yet supported in the Count Files application.\n'
        return False, msg
    else:
        directory = os.path.normpath(os.path.join(os.path.dirname(__file__), 'test'))
        return is_file_utility_available(
            file_path=directory, expected_result=f'{directory}: directory\n')
