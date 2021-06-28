import Helper
import copy


def home():
    return Helper.load_json_file_to_dict('Views/homepage.json')


def custom_markdown(markdown_content):
    view_content = Helper.load_json_file_to_dict('Views/basic_markdown.json')
    view_content['text']['text'] = markdown_content
    return [view_content]


def feature_status(repo, branches):
    feature_status_header = Helper.load_json_file_to_dict('Views/SubViews/featurestatusheader.json')
    feature_status_item = Helper.load_json_file_to_dict('Views/SubViews/featurestatusitem.json')

    feature_status_header['text']['text'] = feature_status_header['text']['text'].format(repo)

    blocks = [
        feature_status_header
    ]

    for branch in branches:
        item = copy.deepcopy(feature_status_item)

        item['text']['text'] = item['text']['text'].format(
            branch.branch_name,
            branch.last_commit_date
        )
        item['accessory']['value'] = repo + ":" + branch.branch_name

        blocks.append(item)

    return blocks
