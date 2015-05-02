|Build Status| |Coverage Status| |PyPI Version| |PyPI Downloads|

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
        In this case, you need to return a tuple, the first arg is True, and the second is a dictionary.'''
        return True, {'text': kwargs['text']}


    def fn2(kwargs):
        '''
        This function shows response the slack post indirectly with an extra post.
        In this case, you need to return a tuple, the first arg is False, and the second is None.
        Now the slack will ignore the response from this request, and if you need do some complex task you can use the built-in slacker.
        For more information, see https://github.com/os/slacker'''
        slackbot.slack.chat.post_message('#general', 'hello from slacker handler')
        return False, None
    slackbot.set_handler(fn1)


    if __name__ == "__main__":
        app.run()


.. |Build Status| image:: https://travis-ci.org/halfcrazy/flask-slackbot.svg?branch=master
   :target: https://travis-ci.org/halfcrazy/flask-slackbot
   :alt: Build Status
.. |PyPI Version| image:: https://img.shields.io/pypi/v/Flask-Slackbot.svg
   :target: https://pypi.python.org/pypi/Flask-SlackBot
   :alt: PyPI Version
.. |PyPI Downloads| image:: https://img.shields.io/pypi/dm/Flask-SlackBot.svg
   :target: https://pypi.python.org/pypi/Flask-SlackBot
   :alt: Downloads
.. |Coverage Status| image:: https://img.shields.io/coveralls/halfcrazy/flask-slackbot.svg
   :target: https://coveralls.io/r/halfcrazy/flask-slackbot
   :alt: Coverage Status
