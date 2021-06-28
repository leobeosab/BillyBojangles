"""
Handles any message logic that the bot will use
"""
import Bitbucket
import Views


def handle_status(message_text):
    """
    Determines a valid status command and builds the blocks
    Should get a command like: @bot status sp-extension

    :param message_text: text of the message
    :returns slack_bolt block object to render to the user
    """

    status_index = message_text.index("status")
    repo_name = message_text[status_index:].replace("status", "").strip()

    branches = Bitbucket.get_current_feature_branches(repo_name)

    if not branches:
        return [
            Views.custom_markdown('*error* could not retrieve branch list for ' + repo_name)
        ]

    if len(branches) == 0:
        return [
            Views.custom_markdown('*All clear champ!* There are no open feature branches for ' + repo_name)
        ]

    return Views.feature_status(repo_name, branches)


def handle_pull_request_creation(action_value):
    """
    This returns a link to create a pull request from a branch to develop
    :param action_value: repo and a feature branch name ex sp-extension:feature/whatever
    :return: a basic string with a link
    """

    payload = action_value.split(":")
    url = Bitbucket.get_create_pull_request_link(payload[0], payload[1], 'develop')

    return f"Here is a link to create a PR from {payload[1]} to develop {url}"
