import os
import requests

import logging

from requests.auth import HTTPBasicAuth
from dataclasses import dataclass

import Helper

BITBUCKET_API_BASE = 'https://api.bitbucket.org/'
BITBUCKET_USER = os.getenv('BITBUCKET_USER')
BITBUCKET_APP_PASSWORD = os.getenv('BITBUCKET_APP_PASSWORD')
BITBUCKET_WORKSPACE = os.getenv('BITBUCKET_WORKSPACE')

HANDY_FILTERS = {
    'feature_branches': 'name~"feature"'
}

logger = logging.getLogger('billybojangles.bitbucket')

def get_branches(repo, query=''):
    URI = '2.0/repositories/{0}/{1}/refs/branches'.format(BITBUCKET_WORKSPACE, repo)
    req = requests.get(BITBUCKET_API_BASE+URI,
                 auth=HTTPBasicAuth(BITBUCKET_USER, BITBUCKET_APP_PASSWORD),
                 params={'q': query})

    if req.status_code == 200:
        raw_branches = req.json()["values"]
        branches = []

        for raw_branch in raw_branches:
            branch = Branch(
                branch_name=raw_branch["name"],
                last_commit_author=raw_branch['target']['author']['raw'],
                last_commit_date=Helper.date_from_bitbucket_date(raw_branch['target']['date']),
                last_commit_hash=raw_branch['target']['hash']
            )

            branches.append(branch)

        return branches
    else:
        logger.error("Failed to get branches for ", repo)
        logger.error(req.text)
        return False


def get_branch(repo, branch_name):
    URI = '2.0/repositories/{0}/{1}/refs/branches/{2}'.format(BITBUCKET_WORKSPACE, repo, branch_name)
    req = requests.get(BITBUCKET_API_BASE + URI,
                       auth=HTTPBasicAuth(BITBUCKET_USER, BITBUCKET_APP_PASSWORD))

    if req.status_code == 200:
        return req.json()
    else:
        logger.error("Failed to get branches for ", repo)
        logger.error(req.text)
        return []


def diff(repo, commit, query=''):
    URI = '2.0/repositories/{0}/{1}/diff/{2}'.format(BITBUCKET_WORKSPACE, repo, commit)
    req = requests.get(BITBUCKET_API_BASE + URI,
                       auth=HTTPBasicAuth(BITBUCKET_USER, BITBUCKET_APP_PASSWORD),
                       params={'q': query})

    if req.status_code == 200:
        return req.text

    if req.status_code == 555:
        return "diff was too large"

    else:
        logger.error(f"Failed to get diff for {repo} @ {commit}")
        logger.error(req.text)
        return None


def get_diff_between_branches(repo, branch_from, branch_to):
    fb = get_branch(repo, branch_from)['target']['hash']
    tb = get_branch(repo, branch_to)['target']['hash']

    d = diff(repo, fb+'..'+tb)

    if d == '':
        return None
    return d


def get_commit(repo, commit_hash):
    URI = '2.0/repositories/{0}/{1}/commit/{2}'.format(BITBUCKET_WORKSPACE, repo, commit_hash)
    req = requests.get(BITBUCKET_API_BASE + URI,
                       auth=HTTPBasicAuth(BITBUCKET_USER, BITBUCKET_APP_PASSWORD))

    if req.status_code == 200:
        return req.json()


def get_current_feature_branches(repo):
    branches = get_branches(repo, HANDY_FILTERS['feature_branches'])

    trimmed_branches = []

    for branch in branches:
        # TODO:// change this to use diffstat instead
        branch_diff = get_diff_between_branches(repo, branch.branch_name, 'develop')
        if branch_diff is None:
            continue

        trimmed_branches.append(branch)

    return trimmed_branches


def get_create_pull_request_link(repo, branch_one, branch_two):
    return f"https://bitbucket.org/{BITBUCKET_WORKSPACE}/{repo}/pull-requests/new?source={BITBUCKET_WORKSPACE}/{repo}%3A%3A{branch_one}&dest={BITBUCKET_WORKSPACE}/{repo}%3A%3A{branch_two}&event_source=branch_detail"


@dataclass
class Branch:
    branch_name: str
    last_commit_author: str
    last_commit_hash: str
    last_commit_date: str
