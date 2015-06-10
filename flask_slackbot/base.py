# coding=utf-8
import cgi

from flask import current_app, Blueprint, request, jsonify, make_response
from slacker import Slacker

from .exceptions import SlackTokenError


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
        bp.add_url_rule(self.callback_url,
                        view_func=self.slack_callback,
                        methods=['POST'])
        self.app.register_blueprint(bp)

    def set_handler(self, fn):
        self.handler = fn

    def filter_outgoing(self, fn):
        self._filter = fn

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

        if hasattr(self, '_filter') and self._filter(text):
            return make_response('', 200)

        try:
            if token != current_app.config.get('SLACK_TOKEN'):
                raise SlackTokenError('unmatch token')
        except SlackTokenError as e:
            return make_response(e.msg, 200)

        '''
        use flag to determine whether response directly,
        or use slacker to deal'''
        rv = self.handler({
            'token': token,
            'team_id': team_id,
            'team_domain': team_domain,
            'channel_id': channel_id,
            'channel_name': channel_name,
            'timestamp': timestamp,
            'user_id': user_id,
            'user_name': user_name,
            'text': text,
            'trigger_word': trigger_word
        })
        if isinstance(rv, dict):
            for key in rv:
                rv.update({key: cgi.escape(rv[key])})
            return jsonify(rv)
        else:
            return make_response('', 200)
