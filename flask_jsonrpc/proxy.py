# -*- coding: utf-8 -*-
# Copyright (c) 2012, Cenobit Technologies, Inc. http://cenobit.es/
# All rights reserved.
import uuid
import urllib
import StringIO

from flask import json, current_app

from flask_jsonrpc.types import Object, Any


class ServiceProxy(object):
    
    def __init__(self, service_url, service_name=None, version='2.0'):
        self.version = str(version)
        self.service_url = service_url
        self.service_name = service_name

    def __getattr__(self, name):
        if self.service_name != None:
            name = '%s.%s' % (self.service_name, name)
        params = dict(self.__dict__, service_name=name)
        return self.__class__(**params)
  
    def __repr__(self):
        return {
            'jsonrpc': self.version,
            'method': self.service_name
        }
    
    def send_payload(self, params):
        """Performs the actual sending action and returns the result
        """
        return urllib.urlopen(self.service_url, json.dumps({
            'jsonrpc': self.version,
            'method': self.service_name,
            'params': params,
            'id': str(uuid.uuid1())
        })).read()
      
    def __call__(self, *args, **kwargs):
        params = kwargs if len(kwargs) else args
        if Any.kind(params) == Object and self.version != '2.0':
            raise Exception('Unsupport arg type for JSON-RPC 1.0 '
                            '(the default version for this client, '
                            'pass version="2.0" to use keyword arguments)')
        r = self.send_payload(params)    
        y = json.loads(r)
        if u'error' in y:
            try:
                if current_app.config['DEBUG']:
                    print '%s error %r' % (self.service_name, y)
            except:
                pass
        return y


class FakePayload(object):
    """
    A wrapper around StringIO that restricts what can be read since data from
    the network can't be seeked and cannot be read outside of its content
    length. This makes sure that views can't do anything under the test client
    that wouldn't work in Real Life.
    """
    def __init__(self, content):
        self.__content = StringIO(content)
        self.__len = len(content)

    def read(self, num_bytes=None):
        if num_bytes is None:
            num_bytes = self.__len or 0
        assert self.__len >= num_bytes, "Cannot read more than the available bytes from the HTTP incoming data."
        content = self.__content.read(num_bytes)
        self.__len -= num_bytes
        return content


class TestingServiceProxy(ServiceProxy):
    """Service proxy which works inside Django unittests
    """
    
    def __init__(self, client, *args, **kwargs):
        super(TestingServiceProxy, self).__init__(*args, **kwargs)
        self.client = client
    
    def send_payload(self, params):
        dump = json.dumps({
            'jsonrpc' : self.version,
            'method' : self.service_name,
            'params' : params,
            'id' : str(uuid.uuid1())
        })
        dump_payload = FakePayload(dump)
        response = current_app.post(self.service_url,
                          **{'wsgi.input' : dump_payload,
                          'CONTENT_LENGTH' : len(dump)})
        return response.content
