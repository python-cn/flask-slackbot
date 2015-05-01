# coding=utf-8
from flask import Flask

from flask_slackbot import SlackBot


app = Flask(__name__)
app.config['SLACK_TOKEN'] = 'Your token here'
app.config['SLACK_CALLBACK'] = '/slack_callback'
app.debug = True
slackbot = SlackBot(app)


def fn1(kwargs):
    return True, {'text': kwargs['text']}


def fn2(kwargs):
    SlackBot.slack.chat.post_message('#general', 'hello from slacker handler')
    return False, None
slackbot.set_handler(fn1)


if __name__ == "__main__":
    app.run()
