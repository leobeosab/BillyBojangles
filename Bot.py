import os
import sys
import logging
from slack_bolt import App

import Views
import Messages

# Setup logging
logger = logging.getLogger("billybojangles")
fh = logging.FileHandler(filename="billybojangles.log")
fh.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)

logger.addHandler(fh)
logger.addHandler(ch)

logger.info('Starting server')

app = App(
    token=os.environ.get('SLACK_BOT_TOKEN'),
    signing_secret=os.environ.get('SLACK_SIGNING_SECRET')
)


@app.event("app_home_opened")
def update_home_tab(client, event, logger):
    try:
        client.views_publish(
            user_id=event["user"],
            view=Views.home()
        )

    except Exception as e:
        logger.error(f"Error publishing home tab: {e}")


@app.event("app_mention")
def mentioned(logger, event, say):
    try:
        if "status" in event['text']:
            say(
                'Sure, let me get you a list of feature branches ahead of develop'
            )
            say(
                blocks=Messages.handle_status(event['text'])
            )
            return

        if "add shortcut" in event['text']:
            say(
                blocks=Messages.handle_add_shortcut(event['text'])
            )
            return

        say('I dunno what you mean fam')
        return


    except Exception as e:
        logger.error(f"Error on app mention {e}")
        say('Error can not do that, Ryan sucks as a dev: ', str(e))


@app.action("create-pull-request")
def create_pull_request(ack, action, say):
    ack()

    say(
        Messages.handle_pull_request_creation(action['value'])
    )




app.start(port=int(os.environ.get("PORT", 3000)))
