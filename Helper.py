import json
import logging

logger = logging.getLogger('billybojangles.helper')


def load_json_file_to_dict(file_path):
    try:
        with open(file_path) as json_file:
            data = json.load(json_file)
            return data
    except Exception:
        logger.error('Could not load ', file_path)
        return {}


def date_from_bitbucket_date(bitbucket_date):
    """
    Strips off timezone and time off of bitbucket dates
    Could be made more robust with datetime

    :param bitbucket_date: date string from bitbucket's api ex: 2021-04-13T13:44:49+00:00
    :returns date string ex: 2021-04-13
    """
    index = bitbucket_date.index("T")
    return bitbucket_date[:index]
