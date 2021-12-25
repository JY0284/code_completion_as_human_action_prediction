import json


class Quad(object):
    def __init__(self):
        self.ctx = []
        self.actor = []
        self.call = []
        self.paras = []
        self.type = ''

    def __str__(self):
        return json.dumps(self.__dict__, indent=4)
