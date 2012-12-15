# -*- coding: utf-8 -*-
# Copyright (c) 2012, Cenobit Technologies, Inc. http://cenobit.es/
# All rights reserved.
from flask import current_app, request, jsonify

def jsonify_status_code(status_code, *args, **kw):
    """Returns a jsonified response with the specified HTTP status code.

    The positional and keyword arguments are passed directly to the
    :func:`flask.jsonify` function which creates the response.

    """
    response = jsonify(*args, **kw)
    response.status_code = status_code
    return response

def extract_raw_data_request(request):
    if request.method == 'GET':
        return request.query_string
    elif request.method == 'POST':
        if request.data:
            return request.data
        elif request.form.to_dict():
            #return '&'.join(['{}={}'.format(k,v) for k,v in request.form.to_dict().items()])
            return request.form.to_dict().keys()[0]
    return ''