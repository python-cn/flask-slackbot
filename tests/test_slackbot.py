# coding=utf-8
import json

from pytest import fixture
from flask import Flask

from flask_slackbot import SlackBot


class App(object):

    def __init__(self):
        self.app = Flask(__name__)
        self.app.debug = True
        self.app.config['SLACK_TOKEN'] = 'Your token here'
        self.app.config['SLACK_CALLBACK'] = '/slack_callback'
        self.slackbot = SlackBot(self.app)
        self.slackbot.set_handler(self.fn)
        self.client = self.app.test_client()

    @staticmethod
    def fn(kwargs):
        return True, {'text': kwargs['text']}


@fixture(scope='module')
def app():
    return App()


def test_response_directly(app):
    rv = app.client.post('/slack_callback', data={
        'token': 'Your token here',
        'text': 'test',
        'team_id': 'team_id',
        'team_domain': 'team_domain',
        'channel_id': 'channel_id',
        'channel_name': 'channel_name',
        'timestamp': 'timestamp',
        'user_id': 'user_id',
        'user_name': 'user_name',
        'trigger_word': 'trigger_word'
    })
    assert rv.status_code == 200
    assert rv.content_type == 'application/json'
    assert json.loads(rv.data)['text'] == 'test'


def test_invalid_token(app):
    rv = app.client.post('/slack_callback', data={
        'token': 'unmatch token',
        'text': 'test',
        'team_id': 'team_id',
        'team_domain': 'team_domain',
        'channel_id': 'channel_id',
        'channel_name': 'channel_name',
        'timestamp': 'timestamp',
        'user_id': 'user_id',
        'user_name': 'user_name',
        'trigger_word': 'trigger_word'
    })

    assert rv.status_code == 200
    assert rv.data == 'unmatch token'
