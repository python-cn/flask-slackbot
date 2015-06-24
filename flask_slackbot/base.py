# coding=utf-8
import sys
from functools import partial

from flask import Blueprint, request, jsonify, make_response
from slacker import Slacker


default_response = partial(make_response, '', 200)
MAX_LENGTH = 1000


class SlackBot(object):

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.slack_chat_token = app.config.get('SLACK_CHAT_TOKEN')

        if self.slack_chat_token:
            self.slack = Slacker(self.slack_chat_token)
        else:
            self.slack = None

        self.callback_url = app.config.get('SLACK_CALLBACK')
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
            return default_response()

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
            if not self.slack:
                return jsonify({'text': 'you have not initialize slacker'})
            attachments = rv.get('attachments', None)
            text = rv['text']
            if sys.version_info.major == 2 and not isinstance(text, str):
                text = text.encode('utf-8')
            if rv.pop('private', False):
                # This will send private message to user
                # If message too long. will raise 414
                if len(text) >= MAX_LENGTH:
                    while text:
                        _text = text[:MAX_LENGTH]
                        text = text[MAX_LENGTH:]
                        self.slack.chat.post_message(user_id, _text,
                                                     attachments=attachments)
                elif len(str(attachments)) >= MAX_LENGTH:
                    for _attachments in zip(*[iter(attachments)] * 10):
                        self.slack.chat.post_message(
                            user_id, text, attachments=list(_attachments))
                else:
                    self.slack.chat.post_message(user_id, rv['text'],
                                                 attachments=attachments)
            elif text:
                return jsonify(rv)
        return default_response()
