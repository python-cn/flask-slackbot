# coding=utf-8
from flask import Flask

from flask_slack_bot import SlackBot


app = Flask(__name__)
app.config['SLACK_TOKEN'] = 'jLGMzrZn3P1lS2sD848KpPuN'
app.config['SLACK_CALLBACK'] = '/slack_callback'
app.debug = True
slackbot = SlackBot(app)


def fn1(kwargs):
    import json
    return True, json.dumps({'text': kwargs['text']})


def fn2(kwargs):
    SlackBot.slack.chat.post_message('#general', 'hello from slacker handler')
    return False, None
slackbot.set_handler(fn1)


if __name__ == "__main__":
    app.run()
