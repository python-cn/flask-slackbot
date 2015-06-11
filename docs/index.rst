Flask-SlackBot
===================

Flask-SlackBot is a Flask extension which helps you deal with slack's outgoing webhook.

Installation
------------
::

    $ pip install flask-slackbot


Usage
-----

.. code-block:: python

    # coding=utf-8 
    from flask import Flask

    from flask_slackbot import SlackBot


    app = Flask(__name__)
    app.config['SLACK_TOKEN'] = 'Your token here'
    app.config['SLACK_CALLBACK'] = '/slack_callback'
    app.debug = True
    slackbot = SlackBot(app)

    '''
    The parameter of the callback function is a dict returns from the slack's outgoing api.
    Here is the detail:
    kwargs
    {
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
    }'''
    def fn1(kwargs):
        '''
        This function shows response the slack post directly without an extra post.
        In this case, you need to return a dict.'''
        return {'text': '!' + kwargs['text']} # Note the '!' character here is an user defined flag to tell the slack, this message is sent from the bot.


    def fn2(kwargs):
        '''
        This function shows response the slack post indirectly with an extra post.
        In this case, you need to return None.
        Now the slack will ignore the response from this request, and if you need do some complex task you can use the built-in slacker.
        For more information, see https://github.com/os/slacker'''
        slackbot.slack.chat.post_message('#general', 'hello from slacker handler')
        return None


    def fn3(text):
        '''
        This function is a filter, which makes our bot ignore the text sent from itself.'''
        return text.startswith('!')

    slackbot.set_handler(fn1)
    slackbot.filter_outgoing(fn3)


    if __name__ == "__main__":
        app.run()


Trap
------------
If you have not set a trigger word, and your callback server return some text to slack, there would be a callback hell. You know like ping pong, and then turn into an infinite loop.

