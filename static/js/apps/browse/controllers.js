(function(App) {
    'use strict';

    var breadcrumbs = function(name) {
        if (name.indexOf('.') !== -1) {
            var names = name.split('.');
            return [names[0], name];
        }
        return [name];
    };

    App.controller('ApplicationCtrl', ['$scope', '$location', 'PendingRequests', 'ContentLoaded', 'Api', function($scope, $location, PendingRequests, ContentLoaded, Api) {
        $scope.response = {
          'status': 200,
          'headers': {
            'content-type': 'application/json',
            'content-length': '113',
            'server': 'Werkzeug/0.8.3 Python/2.7.5',
            'date': 'Fri, 15 Nov 2013 20:15:18 GMT',
            'data': {
              'jsonrpc': '2.0',
              'id': '148c96a5-456c-43ba-a534-ebb0b54311cc',
              'method': 'JSONRPC.welcome',
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
              'method': 'JSONRPC.welcome',
              'params': []
            },
            'headers': {
              'Accept': 'application/json, text/plain, */*',
              'Content-Type': 'application/json;charset=utf-8'
            }
          }
        };
        $scope.response_object = {
          'id': '148c96a5-456c-43ba-a534-ebb0b54311cc', 
          'jsonrpc': '2.0', 
          'result': 'Welcome to Flask JSON-RPC'
        };
        Api.packages(function(packages) {
            $scope.packages = packages;
            ContentLoaded.hide();
        });

        $scope.$on('breadcrumb', function(event, breadcrumb) {
            $scope.breadcrumbs = breadcrumbs(breadcrumb);
        });

        $scope.$emit('breadcrumb', 'dashboard');

        $scope.showContentLoaded = function() {
            return ContentLoaded.isShow();
        };

        $scope.showSpinner = function() {
            return PendingRequests.isPending();
        };

        $scope.routeIs = function(route) {
            if (Object.prototype.toString.call(route) === '[object Array]') {
                for (var i = 0; i < route.length; i++) {
                    if ('/'+route[i] === $location.path()) {
                        return true;
                    }
                }
                return false;
            } 
            return ('/'+route === $location.path());
        };
    }]);

    App.controller('MenuCtrl', ['$scope', '$location', 'Handlebars', function($scope, $location, Handlebars) {
        $scope.showTooltip = function(module) {
            return Handlebars.template('menu-module-tooltip', module);
        };

        $scope.showReponseObject = function(module) {
            return $location.path(module.name);
        };
    }]);

    App.controller('ModuleDialogCtrl', ['$scope', '$modalInstance', 'module', function($scope, $modalInstance, module) {
        $scope.module = module;

        $scope.ok = function() {
            $modalInstance.close(module);
        };

        $scope.hitEnter = function(evt) {
            if (angular.equals(evt.keyCode,13) && !(angular.equals($scope.name,null) || angular.equals($scope.name,''))) {
                $scope.ok();
            }
        };

        $scope.cancel = function() {
            $modalInstance.dismiss('cancel');
        };
    }]);

    App.controller('ResponseObjectCtrl', ['$scope', '$window', '$modal', 'ContentLoaded', 'RPC', 'module', function($scope, $window, $modal, ContentLoaded, RPC, module) {
        $scope.module = module;
        $scope.$emit('breadcrumb', module.name);

        var RPCCall = function(module) {
            RPC.call(module).success(function(response_object, status, headers, config) { // success
                var headers_pretty = headers();
                headers_pretty.data = config.data;

                $scope.response = {status: status, headers: headers_pretty, config: config};
                $scope.response_object = response_object;
                ContentLoaded.hide();
            }).error(function(response_object, status, headers, config) { // error
                var headers_pretty = headers();
                headers_pretty.data = config.data;

                $scope.response = {status_code: status, headers: headers_pretty, config: config};
                $scope.response_object = undefined;
                ContentLoaded.hide();
            });
        };

        if (!module.params || !module.params.length) {
            return RPCCall(module);
        }

        $modal.open({
            templateUrl: 'module_dialog.html',
            controller: 'ModuleDialogCtrl',
            resolve: {
                module: function() {
                    return $scope.module;
                }
            }
        }).result.then(function(module) { // ok
            return RPCCall(module);
        }, function() { // cancel
            $window.history.back();
        });
    }]);

})(window.App);
