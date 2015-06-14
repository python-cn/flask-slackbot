# coding=utf-8
from flask import Flask

from flask_slackbot import SlackBot


app = Flask(__name__)
app.config['SLACK_TOKEN'] = 'Your token here'
# if you need to use slacker you should give a slack chat token
app.config['SLACK_CHAT_TOKEN'] = 'Your slack chat token'
app.config['SLACK_CALLBACK'] = '/slack_callback'
app.debug = True
slackbot = SlackBot(app)


def fn1(kwargs):
    return {'text': '!' + kwargs['text']}


def fn4(kwargs):
        return {'text': '!' + kwargs['text'], 'private': True}


def fn2(kwargs):
    slackbot.slack.chat.post_message('#general', 'hello from slacker handler')
    return None


def fn3(text):
    return text.startswith('!')


slackbot.set_handler(fn1)
slackbot.filter_outgoing(fn3)


if __name__ == "__main__":
    app.run()
