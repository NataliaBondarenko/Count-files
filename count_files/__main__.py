#!/usr/bin/env python3
# encoding: utf-8
"""Count Files.
A command-line interface (CLI) utility.
Supported operating systems: Linux, Mac OS, Windows, Haiku.
It may also be used on iOS (iPhone/iPad) using the StaSh command-line in the Pythonista 3 app.
Main functions:
- total counting of files (total number of files in the directory,
optional: the list of folders in which the found files are located,
and the number of found files in each folder, the total combined size of files found);
- file counting by extension (a table with file extensions sorted by frequency or alphabetically);
- file searching by extension(a list with file paths, optional: file sizes, preview for text files);
- file searching by pattern(a list with file paths, optional: file sizes, preview for text files).
Features:
counting or searching files with a specific extension, files without an extension,
all files regardless of the extension;
recursive and non-recursive counting or searching;
enable or disable the search or counting in hidden files and folders;
process the file extensions with case-sensitive or case-insensitive mode;
enable or disable the program's operating indicator (feedback).

© 2018-2020 Victor Domingos & Nataliia Bondarenko
MIT License
"""
import os
from sys import platform
from argparse import ArgumentParser, Namespace
from typing import TypeVar, Union
from pathlib import Path
from textwrap import fill

from count_files.utils.file_handlers import is_supported_filetype, check_shell_command
from count_files.utils.viewing_modes import show_2columns, show_start_message, \
    show_result_for_total, show_result_for_search_files, show_ext_grouped_by_type
from count_files.platforms import get_current_os
from count_files.settings import SUPPORTED_TYPE_INFO_MESSAGE, NOT_SUPPORTED_TYPE_MESSAGE, \
    DEFAULT_PREVIEW_SIZE, START_TEXT_WIDTH
from count_files.utils.help_system_extension import HelpCmd
from count_files.utils.help_text import topics
from count_files.utils.decorators import exceptions_decorator
from count_files.utils.group_extensions import ext_and_group_dict


parser = ArgumentParser(
    prog='count-files',
    description='Count files, grouped by extension, in a directory. By '
                'default, it will count files recursively in current '
                'working directory and all of its subdirectories, and '
                'will display a table showing the frequency for each file '
                'extension (e.g.: .txt, .py, .html, .css) and the total '
                'number of files found. For supported operating systems '
                '(Linux, Mac OS, iOS, Windows, Haiku), '
                'any hidden files or folders are ignored by default. '
                'For other operating systems this option is not available, '
                'and as a result all existing files will be included. '
                'Also by default file extensions are treated with no case sensitiveness.')

parser.add_argument('-v', '--version', action='version', version=__import__('count_files').__version__)

parser.add_argument('-st', '--supported-types', action='store_true',
                    help=topics['supported-types']['short'])

parser.add_argument('path', nargs='?', default=os.getcwd(), type=str,
                    help=topics['path']['short'])

parser.add_argument('-a', '--all', action='store_true', default=False,
                    help=topics['all']['short'])

parser.add_argument('-nr', '--no-recursion', action='store_true', default=False,
                    help=topics['no-recursion']['short'])

parser.add_argument('-c', '--case-sensitive', action='store_true', default=False,
                    help=topics['case-sensitive']['short'])

parser.add_argument('-nf', '--no-feedback', action='store_true', default=False,
                    help=topics['no-feedback']['short'])

parser.add_argument('-hc', '--help-cmd', action='store_true', default=False,
                    help=topics['help-cmd']['short'])


total_group = parser.add_argument_group('Total number of files'.upper(),
                                        description=topics['total-group']['short'])

total_group.add_argument('-t', '--total', dest="extension", type=str,
                         help=topics['total']['short'])

total_group.add_argument('-sf', '--show-folders', action='store_true', default=False,
                         help=topics['show-folders']['short'])

total_group.add_argument('-ts', '--total-size', action='store_true', default=False,
                         help=topics['total-size']['short'])


count_group = parser.add_argument_group('File counting by extension'.upper(),
                                        description=topics['count-group']['short'])

count_group.add_argument('-alpha', '--sort-alpha', action='store_true', default=False,
                         help=topics['sort-alpha']['short'])

count_group.add_argument('-g', '--group', action='store_true', default=False,
                         help=topics['group']['short'])

search_group = parser.add_argument_group('File searching by extension or by pattern'.upper(),
                                         description=topics['search-group']['short'])

search_group.add_argument('-fe', '--file-extension', type=str,
                          help=topics['file-extension']['short'])

search_group.add_argument('-fm', '--filename-match', type=str, dest='pattern',
                          help=topics['filename-match']['short'])

search_group.add_argument('-p', '--preview', action='store_true', default=False,
                          help=topics['preview']['short'])

search_group.add_argument('-ps', '--preview-size', type=int, default=DEFAULT_PREVIEW_SIZE,
                          help=topics['preview-size']['short'])

search_group.add_argument('-fs', '--file-sizes', action='store_true', default=False,
                          help=topics['file-sizes']['short'])

search_group.add_argument('-sc', '--shell-command', type=str, default=False, choices=['file'],
                          help=topics['shell-command']['short'])

parser._positionals.title = parser._positionals.title.upper()
parser._optionals.title = parser._optionals.title.upper()

argparse_namespace_object = TypeVar('argparse_namespace_object', bound=Namespace)


@exceptions_decorator
def main_flow(*args: [argparse_namespace_object, Union[bytes, str]]):
    """Main application function.

    :param args: object <class 'argparse.Namespace'>,
    for tests param args - list with objects of <class 'str'>
    :return:
    Returns the processed data as text to the screen.
    Total number of files, table or list with file paths.
    Returns parser.exit(status=1):
    if path does not exist or there may be a typo in it,
    if the path has hidden folders and the argument --all is not specified,
    if the preview is not available for the specified file type,
    if the "file" command is not available or does not work as expected.
    """
    args = parser.parse_args(*args)
    recursive = not args.no_recursion
    include_hidden = args.all
    sort_alpha = args.sort_alpha
    extension = args.file_extension
    current_os = get_current_os()
    if current_os.name == 'BaseOS':
        # the default option to exclude hidden files and folders is not implemented for undefined OS,
        # no need to call self.is_hidden_file_or_dir()
        include_hidden = True

    if args.supported_types:
        parser.exit(status=0, message=SUPPORTED_TYPE_INFO_MESSAGE)

    if args.help_cmd:
        hc = HelpCmd()
        hc.cmdloop()
        parser.exit(status=0)

    if os.path.abspath(args.path) == os.getcwd():
        location = os.getcwd()
        loc_text = ' the current directory'
    else:
        location = os.path.expanduser(args.path)
        loc_text = ':\n' + os.path.normpath(location)

    if not os.path.exists(location):
        parser.exit(status=1, message=f'The path {location} '
                                      f'does not exist, or there may be a typo in it.')

    if not include_hidden and current_os.is_hidden_file_or_dir(location):
        # skip check if path is a local drive
        if platform.startswith('win') and len(Path(location).parents) == 0:
            pass
        else:
            parser.exit(status=1, message=f'\nNot counting any files, because {loc_text[2:]}'
                                          f' has hidden folders.\n'
                                          f'Use the --all argument to include hidden files and folders.')

    if args.preview and args.shell_command:
        # check for Unix "file" command
        preview_with_file, msg = check_shell_command()
        if not preview_with_file:
            parser.exit(status=1, message=msg)
    else:
        preview_with_file = False  # assigning this local variable to pass the parser test

    print("")
    # Parser total_group
    # getting the total number of files for -t .. (all extensions), -t . and -t extension_name
    if args.extension:
        print(fill(show_start_message(args.extension, args.case_sensitive, recursive,
                                      include_hidden, location, 'total'),
                   width=START_TEXT_WIDTH),
              end="\n\n")
        data = current_os.search_files(dirpath=location,
                                       extension=args.extension,
                                       include_hidden=include_hidden,
                                       recursive=recursive,
                                       case_sensitive=args.case_sensitive)
        total_result = show_result_for_total(data, total_size=args.total_size,
                                             show_folders=args.show_folders,
                                             no_feedback=args.no_feedback,
                                             recursive=recursive)
        return total_result

    # Parser search_group: search file names by pattern, --filename-match
    if args.pattern:
        print(fill(show_start_message(args.pattern, args.case_sensitive, recursive,
                                      include_hidden, location, 'pattern'),
                   width=START_TEXT_WIDTH),
              end="\n\n")

        # getting data list with Unix shell-style wildcards: *, ?, [seq], [!seq]
        data = current_os.search_files_by_pattern(dirpath=location,
                                                  pattern=args.pattern,
                                                  recursive=recursive,
                                                  include_hidden=include_hidden,
                                                  case_sensitive=args.case_sensitive)

        # preview behavior is similar to --file-extension .. (all extensions)
        # in this case, the preview will only be displayed for files with a supported extension
        len_files = show_result_for_search_files(files=data,
                                                 file_sizes=args.file_sizes,
                                                 preview=args.preview,
                                                 preview_size=args.preview_size,
                                                 preview_with_file=preview_with_file)

        return len_files

    # Parser search_group: search and list files by extension, --file-extension
    if extension:
        print(fill(show_start_message(extension, args.case_sensitive, recursive, include_hidden, location),
                   width=START_TEXT_WIDTH),
              end="\n\n")
        if args.preview and preview_with_file is False:
            if extension == '.' or not is_supported_filetype(extension.lower()):
                parser.exit(status=1, message=NOT_SUPPORTED_TYPE_MESSAGE)

        # getting data list for -fe .. (all extensions), -fe . and -fe extension_name
        data = (f for f in current_os.search_files(dirpath=location,
                                                   extension=extension,
                                                   include_hidden=include_hidden,
                                                   recursive=recursive,
                                                   case_sensitive=args.case_sensitive))
        # display the result as a list
        len_files = show_result_for_search_files(files=data,
                                                 file_sizes=args.file_sizes,
                                                 preview=args.preview,
                                                 preview_size=args.preview_size,
                                                 preview_with_file=preview_with_file)

        return len_files

    # Parser count_group: counting all files by extension
    print(fill(show_start_message(None, args.case_sensitive, recursive, include_hidden, location),
               width=START_TEXT_WIDTH),
          end="\n\n"
          )
    data = current_os.count_files_by_extension(dirpath=location,
                                               no_feedback=args.no_feedback,
                                               include_hidden=include_hidden,
                                               recursive=recursive,
                                               case_sensitive=args.case_sensitive)

    # if empty sequence
    if not data:
        parser.exit(status=0, message='No files were found in the specified directory.\n')
        
    total_occurrences = sum(data.values())
    max_word_width = max(map(len, data.keys()))

    # display the result as a list of two columns
    if args.group:
        if sort_alpha:
            # sort extensions alphabetically, with uppercase versions on top
            sort_key = lambda data: (data[0].casefold(), data[0])
            data = sorted(data.items(), key=sort_key)
            show_ext_grouped_by_type(data=data, ext_and_group=ext_and_group_dict)
        else:
            # sort extensions by group and by frequency in each group
            show_ext_grouped_by_type(data=data.most_common(), ext_and_group=ext_and_group_dict)
        print(f'\n  Found {total_occurrences} file(s).')
        parser.exit(status=0)
    # display the result as a table
    elif sort_alpha:
        # sort extensions alphabetically, with uppercase versions on top
        sort_key = lambda data: (data[0].casefold(), data[0])
        data = sorted(data.items(), key=sort_key)
        show_2columns(data, max_word_width, total_occurrences)
        parser.exit(status=0)
    else:
        # sort extensions by frequency for each file extension
        data = data.most_common()
        show_2columns(data, max_word_width, total_occurrences)
        parser.exit(status=0)


if __name__ == "__main__":
    main_flow()
