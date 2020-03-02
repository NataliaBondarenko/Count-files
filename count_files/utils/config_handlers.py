import os
import itertools
from textwrap import fill
from typing import List, Tuple, Dict

from count_files.utils.ini_template import generate_ini_file
from count_files.settings import START_TEXT_WIDTH


def confirm_action(question: str, start_message: str =None,
                   func=None, end_message: str =None, func_kwargs=None) -> bool:
    if start_message:
        print(fill(start_message, width=START_TEXT_WIDTH, initial_indent=' ' * 2, subsequent_indent=' ' * 2))
    answer = input(question)
    if answer.lower() in ['y', 'yes']:
        if func:
            if func_kwargs:
                    func(**func_kwargs)
            else:
                func()
        if end_message:  # success
            print(end_message)
        return True
    else:
        return False


def get_correct_location(args):
    """Handles the case when the positional argument "path" can fall into the list of types.

    ArgumentParser 'append' action - This stores a list, and appends each argument value to the list.
    This is useful to allow an option to be specified multiple times.
    :param args: all parser args
    :return:
    """
    types_list = list(itertools.chain.from_iterable(args.type))
    # TODO
    paths = [x for x in types_list if '/' in x or '\\' in x or ':' in x or '~' in x]
    if paths:
        print("\nPossible values for the positional argument 'path' were found in the type list.")
        for i in paths:
            print(f"  '{i}'")
        print(fill("If you explicitly specify the path to the folder, "
                   "then it should not be after the argument --sort-type "
                   "so that it does not fall into the list of types. "
                   "Please specify the path before the '--sort-type' argument."))
        # parser.exit()
        return None, None
    else:
        location = args.path
    if os.path.abspath(location) == os.getcwd():
        location = os.getcwd()
        loc_text = ' the current directory'
    else:
        location = os.path.expanduser(location)
        loc_text = ':\n' + os.path.normpath(location)
    return location, loc_text


def sort_ext_by_type(data: List[Tuple[str, int]],
                     ext_and_type_dict: Dict[str, str],
                     type_and_ext_storage: Dict[str, list]) -> Dict[str, List[Tuple[str, int]]]:
    """Sorting extensions by type.

    Types are user-defined extension groups in the configuration file.

    :param data: list with items like [('png', 8), ('txt', 25), ...]
    :param ext_and_type_dict: dict with items like {'png': 'image', 'txt': documents, ...}
    :param type_and_ext_storage: dict with items like {'images': [], 'documents': [], ...}
     key - type name, value - empty list
    :return: dict with items like {'images': [('png', 8), ...], 'documents': [('txt', 25), ...], ...}
    """
    for (ext, freq) in data:
        item_type = ext_and_type_dict.get(ext, '+ + ')
        type_and_ext_storage[item_type].append((ext, freq))
    return type_and_ext_storage


def prepare_templates(types_list: List[str], case_sensitive: bool,
                      config_parser) -> Tuple[Dict[str, list], Dict[str, str]]:
    """Create templates required for sorting extensions by type.

    1) type_and_ext_storage
    dict with items like {'images': [], 'documents': [], ...}
    key - type name, value - empty list
    updated in def sort_ext_by_type to store (ext, freq) tuples
    2) ext_and_type_dict
    dict with items like {'png': 'image', 'txt': documents, ...}
    used to get type for counted extensions in def sort_ext_by_type

    :param types_list: args.type
    :param case_sensitive: args.case_sensitive
    :param config_parser: configparser.ConfigParser
    :return: dicts
    """
    type_and_ext_storage = {}
    ext_and_type_dict = {}
    # types_list - values entered by user, `--sort-type images data`
    etd_keys = ext_and_type_dict.keys()
    for item in types_list:
        s: str = config_parser.get(item, 'extensions')
        if not case_sensitive:
            s = s.upper()
        ext_list = [x.strip() for x in s.strip().split(',')]
        for ext in ext_list:
            if ext in etd_keys:
                # skip duplicates in groups
                continue
            ext_and_type_dict.update({ext: item})
        type_and_ext_storage.update({item: []})
    # '+ + ' is a key for other files
    type_and_ext_storage.update({'+ + ': []})
    return type_and_ext_storage, ext_and_type_dict


def get_available_sections(types_list: List[str], config_path: str, config_parser) -> List[str]:
    """Checking entries in the configuration file before starting file counting.

    :param types_list: args.type
    :param config_path: configuration file path
    :param config_parser:
    :return: configparser.ConfigParser
    """
    start_types_list = types_list
    sections: list = config_parser.sections()
    if not sections:
        print(f"No records in configuration file {config_path}")
        return []
    new_types_list = []
    for i in types_list:
        if i in sections:
            if config_parser.has_option(i, 'extensions'):
                if config_parser[i]['extensions']:
                    new_types_list.append(i)
    # get not available sections
    diff = [x for x in start_types_list if x not in new_types_list]
    if diff:
        for d in diff:
            if d not in sections:
                print(f"The '{d}' section does not exist.")
            else:
                print(f"Section '{d}' has no extensions.")
        if len(diff) == len(start_types_list):
            return []
        if confirm_action(start_message=f"Not available section(s): {str(diff)[1:-1]} "
                                        f"in configuration file {config_path}\n"
                                        f"You can sort by available sections: {str(new_types_list)[1:-1]}",
                          question=f"Continue? [y/n]: "):
            return new_types_list
        else:
            return []
    return new_types_list


def init_sort_by_type(types_list: list, config_path: str, file_exist: bool):
    """Create or restore the default configuration file.

    :param types_list: args.type
    :param config_path: configuration file path
    :param file_exist: does the configuration file exist
    :return:
    """
    if 'default' in types_list:
        start_message = f"You entered the value 'default' with the '--sort-type' argument. " \
                        f"This action begins the process of creating a default configuration file " \
                        f"with a description and examples. " \
                        f"File {config_path} {'already exists' if file_exist else 'does not exist'}."
        question = f"{'Completely overwrite' if file_exist else 'Create'} count_files.ini file? [y/n]: "
        end_message = f"\nFile {config_path} was {'overwritten' if file_exist else 'created.'}."
        if confirm_action(start_message=start_message, question=question,
                          func=generate_ini_file, end_message=end_message):
            return
        else:
            print(f"\nThe file was not "
                  f"{'overwritten' if file_exist else 'created. You cannot sort extensions by type.'}.\n")
            return
    elif not file_exist:
        start_message = f"Configuration file {config_path} does not exist. " \
                        f"This file must exist and contain the data necessary to sort the file extensions by type. " \
                        f"This action begins the process of creating count_files.ini file " \
                        f"with a description and examples."
        question = 'Create default count_files.ini file? [y/n]: '
        end_message = f"\nFile {config_path} created."
        if confirm_action(start_message=start_message, question=question,
                          func=generate_ini_file, end_message=end_message):
            return
        else:
            print(f"\nFile does not exist. You cannot sort extensions by type.\n")
            return
    else:
        return
