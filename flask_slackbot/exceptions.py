# coding=utf-8
class SlackTokenError(Exception):

    def __init__(self, msg):
        self.msg = msg


class NoSlackerError(Exception):

    def __init__(self, msg):
        self.msg = msg
