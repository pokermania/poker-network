# -*- coding: utf-8 *-*

class Node(object):

    def update(self, _dict):
        for k, v in _dict.items():
            if isinstance(v, dict):
                if k not in self.__dict__ or not isinstance(self.__dict__[k], Node):
                    self.__dict__[k] = Node()
                self.__dict__[k].update(v)
            else:
                self.__dict__[k] = v

    def __repr__(self):
        return '<Node>'

class Config(Node):

    def __init__(self, _dict=None):
        if _dict:
            self.update(_dict)

    def __repr__(self):
        return '<Config>'

# config finder
import os

def find_config(_path, _file):
    while True:
        _fpath = os.path.join(_path, _file)
        if os.path.exists(_fpath):
            return _fpath
        if len(_path) < 2:
            return None
        _path = os.path.abspath(os.path.join(_path, '..'))

# search default.json, config.json
dpath = find_config(os.getcwd(), 'default.json')
cpath = find_config(os.getcwd(), 'config.json')

if not dpath:
    raise Exception('couldn\'t find default.json in this or any parent directory')

# load conifg
from simplejson import loads as decode

config = Config(decode(open(dpath, 'r').read()))
if cpath:
    config.update(decode(open(cpath, 'r').read()))

__all__ = ['config']