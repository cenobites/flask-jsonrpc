(function(App) {
    'use strict';

    angular.module('browse.service', ['ngResource'])
        .constant('urlPrefix', _URL_PREFIX)
        .constant('serverUrls', _SERVER_URLS)
        .constant('responseExample', {
          'status': 200,
          'headers': {
            'content-type': 'application/json',
            'content-length': '113',
            'server': 'Werkzeug/0.8.3 Python/2.7.5',
            'date': 'Fri, 15 Nov 2013 20:15:18 GMT',
            'data': {
              'jsonrpc': '2.0',
              'id': '148c96a5-456c-43ba-a534-ebb0b54311cc',
              'method': 'Api.welcome',
              'params': []
            }
          },
          'config': {
            'transformRequest': [
              null,
              null
            ],
            'transformResponse': [
              null
            ],
            'method': 'POST',
            'url': '/api',
            'data': {
              'jsonrpc': '2.0',
              'id': '148c96a5-456c-43ba-a534-ebb0b54311cc',
              'method': 'Api.welcome',
              'params': []
            },
            'headers': {
              'Accept': 'application/json, text/plain, */*',
              'Content-Type': 'application/json;charset=utf-8'
            }
          }
        })
        .constant('responseObjectExample', {
          'id': '148c96a5-456c-43ba-a534-ebb0b54311cc',
          'jsonrpc': '2.0',
          'result': 'Welcome to Flask JSON-RPC'
        })
        .value('Toolbar', {
            value: false,
            show: function() {
                this.value = true;
            },
            hide: function() {
                this.value = false;
            },
            isShow: function() {
                return this.value;
            }
        })
        .factory('Api', ['$resource', 'urlPrefix', function($resource, urlPrefix) {
            return $resource(urlPrefix + '/:service.json', {}, {
                packages: {method: 'GET', params: {service: 'packages'}},
                method: {method: 'GET', params: {service: 'method'}}
            });
        }])
        .factory('UUID', [function() {
            return {
                uuid4: function() {
                    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
                        var r = Math.random()*16|0, v = c == 'x' ? r : (r&0x3|0x8);
                        return v.toString(16);
                    });
                }
            };
        }])
        .factory('RPC', ['$http', '$location', 'serverUrls', 'UUID', function($http, $location, serverUrls, UUID) {
            return {
                getValue: function(param) {
                    if (!param.value) {
                        return param.value;
                    }

                    if (param.type === 'Object') {
                        return eval('('+ param.value + ')');
                    } else if (param.type === 'Number') {
                        if (param.value.indexOf('.') !== -1) {
                            return parseFloat(param.value);
                        }
                        return parseInt(param.value);
                    } else if (param.type === 'Boolean') {
                        return (/^(true|1)$/i).test(param.value);
                    } else if (param.type === 'String') {
                        return param.value;
                    } else if (param.type === 'Array') {
                        return eval('(' + param.value + ')');
                    } else if (param.type === 'Null') {
                        return null;
                    }
                    return param.value;
                },
                payload: function(module, options) {
                    var payload = {
                        jsonrpc: '2.0',
                        method: module.name,
                        params: {}
                    };

                    if (!module.notify) {
                        payload.id = UUID.uuid4();
                    }

                    if (!module.params || !module.params.length) {
                        payload.params = [];
                        return payload;
                    }

                    for (var i = 0; i < module.params.length; i++) {
                        payload.params[module.params[i].name] = this.getValue(module.params[i]);
                    }

                    return payload;
                },
                callWithPayload: function(data, options) {
                    var serviceUrl = serverUrls[data.method];
                    var options = options || {method: 'POST', url: serviceUrl};
                    options.data = data;
                    return $http(options);
                },
                call: function(module, options) {
                    return this.callWithPayload(this.payload(module, options), options);
                },
            };
        }]);

})(window.App);
