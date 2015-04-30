# coding=utf-8
from flask import current_app, Blueprint, request, make_response
from flask.views import MethodView

from slacker import Slacker


class SlackBot(object):

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.slack_token = app.config.get('SLACK_TOKEN')
        self.callback_url = app.config.get('SLACK_CALLBACK')
        self.slack = Slacker(self.slack_token)
        self.init_bp()

    def init_bp(self):
        bp = Blueprint('slack', __name__)
        bp.add_url_rule(self.callback_url, view_func=self.slack_callback, methods=['POST'])
        self.app.register_blueprint(bp)

    def set_handler(self, fn):
        self.handler = fn

    def slack_callback(self):
        token = request.form.get('token')
        team_id = request.form.get('team_id')
        team_domain = request.form.get('team_domain')
        channel_id = request.form.get('channel_id')
        channel_name = request.form.get('channel_name')
        timestamp = request.form.get('timestamp')
        user_id = request.form.get('user_id')
        user_name = request.form.get('user_name')
        text = request.form.get('text')
        trigger_word = request.form.get('trigger_word')

        if token != current_app.config.get('SLACK_TOKEN'):
            raise Exception('unmatch token')

        # use flag to determine whether response directly, or use slacker to deal
        flag, d = self.handler({
            'token': token,
            'team_id': team_id,
            'team_domain': team_domain,
            'channel_id': channel_id,
            'channel_name': channel_name,
            'timestamp': timestamp,
            'user_id': user_name, 
            'user_name': user_name,
            'text': text, 
            'trigger_word': trigger_word
        })
        if flag:
            resp = make_response(d, '200')
            resp.headers['Content-Type'] = 'application/json'
            return resp
        else:
            return ''
