import json

PAD_TOKEN = '<PAD>'
CALL_TOKEN = '<Call>'
ASSIGN_TOKEN = '<Assign>'
RETURN_TOKEN = '<Return>'
CONST_TOKEN = '$Const$'
SELF_TOKEN = '$'

"""
Length limitations for call extractor.
"""
MAX_ASSIGN_LEFT_VALUE = 3
MAX_PARA_CONSTANT_LEN = 5


"""
Length limitations for quad fields(for storage, 
different with length using in data processing.).
"""
STORAGE_MAX_CTX_LEN = 7
STORAGE_MAX_CALL_LEN = 7
STORAGE_MAX_ACTOR_LEN = 3
STORAGE_MAX_TYPE_LEN = 1
STORAGE_MAX_PARAS_LEN = 3

class Quad(object):
    def __init__(self):
        self.ctx = []
        self.actor = []
        self.call = []
        self.paras = []
        self.type = ''

    def __str__(self):
        return json.dumps(self.__dict__, indent=4)
