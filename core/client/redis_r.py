#!/usr/bin/env python
# -*- coding: utf-8 -*-

import redis
import ketama
import re

from common.rpc_proxy import RPCProxy
from utils.md5 import get_md5

rs_clients = {}

class RedisRing(object):
    __slots__ = ('server_list', 'continuum')
    SERVERS = {}
    def __init__(self, ketama_server_file):
        self.server_list = self.parse_server_file(ketama_server_file)
        self.continuum = ketama.Continuum(ketama_server_file)

        for server in self.server_list:
            connection = redis.StrictRedis(host = server[0], port = int(server[1]), db=0)
            server_string = server[0] + ":" + server[1]
            RedisRing.SERVERS.update({
                server_string : connection,
            })

    def get_con(self, key):
        server = self.continuum.get_server(key)
        return RedisRing.SERVERS.get(server[1])

    def parse_server_file(self, ketama_server_file):
        with open(ketama_server_file, 'r') as f:
            file_content = f.read()
            result = re.findall('([^:]*):([^\s]*)\s[^\n]*\n', file_content)
            return result

def get_redis_client(filename, max_conn_num=30):
    content = ''
    with open(filename, 'r') as f:
        content = f.readlines()
    key = get_md5(content)

    global rs_clients
    if key not in rs_clients:
        params = {'ketama_server_file':filename}
        proxy = RPCProxy(cls=RedisRing, max_conn_num=max_conn_num, **params)
        rs_clients[key] = proxy
    return rs_clients[key]
