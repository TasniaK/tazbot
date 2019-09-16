from flask import Flask
import config

import time
from slackclient import SlackClient

app = Flask(__name__)
app.secret_key = config.SECRET_KEY

# instantiate Slack client os.environ.get('SLACK_BOT_TOKEN')
slack_client = SlackClient(config.SLACK_BOT_TOKEN)
# tazbot's user ID in Slack: value is assigned after the bot starts up
tazbot_id = None

# constants
RTM_READ_DELAY = 1 # 1 second delay between reading from RTM
EXAMPLE_COMMAND = 'create'
MENTION_REGEX = '^<@(|[WU].+?)>(.*)'

@app.route('/')
def hello():
    return "tazbot here"

# if 'create' command
def parse_bot_commands(slack_events):
    """
        Parses message events from the Slack RTM API.
        If trigger words found, this function replys with a corresponding gif.
        If no trigger messages are found, then this function returns None.
    """
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            message = event["text"]
            return message
            # if message == 'testtazcommand':
            #     return message
    return None

# if 'update' command

if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("tazbot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            message = parse_bot_commands(slack_client.rtm_read())
            print(message)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")