import json
import logging

logger = logging.getLogger('billybojangles.helper')


def load_json_file_to_dict(file_path):
    try:
        with open(file_path) as json_file:
            data = json.load(json_file)
            return data
    except Exception as e:
        logger.error(f'Could not load {file_path} {e}')
        return {}


def dump_dict_to_json_file(dict, file_path):
    try:
        with open(file_path, 'w') as json_file:
            json.dump(dict, json_file)
    except Exception as e:
        logger.error(f'Could not write to {file_path} {e}')


def date_from_bitbucket_date(bitbucket_date):
    """
    Strips off timezone and time off of bitbucket dates
    Could be made more robust with datetime

    :param bitbucket_date: date string from bitbucket's api ex: 2021-04-13T13:44:49+00:00
    :returns date string ex: 2021-04-13
    """
    index = bitbucket_date.index("T")
    return bitbucket_date[:index]


def get_repo_shortcut(repo_name):
    """
    Gets a shortcut for a repo and returns it if it exists
    if it doesn't exist it returns the original name
    :param repo_name:
    :returns shortcut or repo_nme if shortcut doesn't exist
    """
    shortcuts = load_json_file_to_dict('./repo-shortcuts.json')

    try:
        return shortcuts[repo_name]
    except KeyError:
        return repo_name
