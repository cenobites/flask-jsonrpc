(function(App) {
    'use strict';

    var breadcrumbs = function(name) {
        if (name.indexOf('.') !== -1) {
            var names = name.split('.');
            return [names[0], name];
        }
        return [name];
    };

    App.controller('ApplicationCtrl', ['$scope', '$location', 'responseExample', 'responseObjectExample', 'PendingRequests', 'ContentLoaded', 'Toolbar', function($scope, $location, responseExample, responseObjectExample, PendingRequests, ContentLoaded, Toolbar) {
        Toolbar.hide();

        $scope.response = responseExample;
        $scope.response_object = responseObjectExample;

        $scope.$on('App:breadcrumb', function(event, breadcrumb) {
            $scope.breadcrumbs = breadcrumbs(breadcrumb);
        });

        $scope.$emit('App:breadcrumb', 'Dashboard');

        $scope.showContentLoaded = function() {
            return ContentLoaded.isShow();
        };

        $scope.showSpinner = function() {
            return PendingRequests.isPending();
        };

        $scope.showToolbar = function() {
            return Toolbar.isShow();
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

    App.controller('MenuCtrl', ['$scope', '$location', 'Handlebars', 'ContentLoaded', 'Api', function($scope, $location, Handlebars, ContentLoaded, Api) {
        ContentLoaded.show();
        Api.packages(function(packages) {
            $scope.packages = packages;
            ContentLoaded.hide();
        });

        $scope.showTooltip = function(module) {
            return Handlebars.template('menu-module-tooltip', module);
        };

        $scope.showReponseObject = function(module) {
            return $location.path(module.name);
        };
    }]);

    App.controller('ViewerContainerCtrl', ['$scope', '$location', 'Toolbar', function($scope, $location, Toolbar) {
        $scope.resend = function() {
            $scope.$broadcast('RPC:resend');
        };

        $scope.changeParameters = function() {
            $scope.$broadcast('RPC:changeParameters');
        };

        $scope.notify = function() {
            $scope.$broadcast('RPC:notify');
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

    App.controller('ResponseObjectCtrl', ['$scope', '$window', '$modal', 'ContentLoaded', 'Toolbar', 'RPC', 'module', function($scope, $window, $modal, ContentLoaded, Toolbar, RPC, module) {
        Toolbar.show();
        $scope.module = module;
        $scope.$emit('App:breadcrumb', module.name);

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
        },
        RPCCallModal = function(module) {
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
                ContentLoaded.hide();
                $window.history.back();
            });
        };

        $scope.$on('RPC:resend', function(event) {
            return RPCCall($scope.module);
        });
        
        $scope.$on('RPC:changeParameters', function(event) {
            return RPCCallModal($scope.module);
        });

        $scope.$on('RPC:notify', function(event) {
            var m = angular.copy($scope.module);
            m.notify = true;
            return RPCCall(m);
        });

        if (!module.params || !module.params.length) {
            return RPCCall(module);
        }

        return RPCCallModal(module);
    }]);

})(window.App);
