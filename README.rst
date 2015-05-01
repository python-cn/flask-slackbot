
[WIP]Flask-SlackBot
===================

Flask-SlackBot is a Flask extension which helps you deal with slack's outgoing webhook.

Installation
------------
::

    $ pip install flask-slackbot


Usage
-----
::

    # coding=utf-8 
    from flask import Flask

    from flask_slackbot import SlackBot


    app = Flask(__name__)
    app.config['SLACK_TOKEN'] = 'Your token here'
    app.config['SLACK_CALLBACK'] = '/slack_callback'
    app.debug = True
    slackbot = SlackBot(app)


    def fn1(kwargs):
        '''
        This function shows response the slack post directly without an extra post.
        In this case, you need to return a tuple, the first arg is True, and the second is a json.'''
        import json
        return True, json.dumps({'text': kwargs['text']})


    def fn2(kwargs):
        '''
        This function shows response the slack post indirectly with an extra post.
        In this case, you need to return a tuple, the first arg is False, and the second is None.
        Now the slack will ignore the response from this request, and if you need do some complex task you can use the built-in slacker.
        For more information, see https://github.com/os/slacker'''
        SlackBot.slack.chat.post_message('#general', 'hello from slacker handler')
        return False, None
    slackbot.set_handler(fn1)


    if __name__ == "__main__":
        app.run()

