"""
Handles any message logic that the bot will use
"""
import Bitbucket
import Views
import Helper


def handle_status(message_text):
    """
    Determines a valid status command and builds the blocks
    Should get a command like: @bot status sp-extension

    :param message_text: text of the message
    :returns slack_bolt block object to render to the user
    """

    status_index = message_text.index("status")
    repo_name = message_text[status_index:].replace("status", "").strip()

    repo_name = Helper.get_repo_shortcut(repo_name)

    branches = Bitbucket.get_current_feature_branches(repo_name)

    if not branches:
        return Views.custom_markdown('*Error* could not retrieve branch list for ' + repo_name)

    if len(branches) == 0:
        return Views.custom_markdown('*All clear champ!* There are no open feature branches for ' + repo_name)


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


def handle_add_shortcut(message_text):
    """
    Updates the repo-shortcuts json with a new shortcut
    :param message_text: string message fromt the user
    :returns None
    """

    add_index = message_text.index('add shortcut')
    command = message_text[add_index:].replace('add shortcut', '').strip()

    input = command.split(' ')

    if len(input) != 2:
        return Views.custom_markdown('*Error* you must add a shortcut like: spapi smarterproctoring-api-v2')

    current_shortcuts = Helper.load_json_file_to_dict('./repo-shortcuts.json')
    current_shortcuts[input[0]] = input[1]

    Helper.dump_dict_to_json_file(current_shortcuts, './repo-shortcuts.json')

    return Views.custom_markdown(f'Shortcut {input[0]}->{input[1]} has been added :pray:')