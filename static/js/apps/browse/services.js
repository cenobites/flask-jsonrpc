(function(App) {
    'use strict';

    angular.module('browse.service', ['ngResource'])
        .factory('Api', ['$resource', function($resource) {
            return $resource('/browse/:service.json', {}, {
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
        .factory('RPC', ['$http', 'UUID', function($http, UUID) {
            return {
                _call: function(data, options) {
                    var serviceUrl = 'api',
                        options = options || {method: 'POST', url: '/' + serviceUrl};
                    options.data = data;
                    return $http(options);
                },
                payload: function(module, options) {
                    var payload = {
                        jsonrpc: '2.0', 
                        id: UUID.uuid4(), 
                        method: module.name, 
                        params: {}
                        //params: []
                    };

                    if (!module.params || !module.params.length) {
                        payload.params = [];
                        return payload;
                    }

                    for (var i = 0; i < module.params.length; i++) {
                        payload.params[module.params[i].name] = module.params[i].value;
                        //payload.params.push(module.params[i].value);

                    }

                    return payload;
                },
                call: function(module, options) {
                    return this._call(this.payload(module, options), options);
                }
            };
        }]);

})(window.App);