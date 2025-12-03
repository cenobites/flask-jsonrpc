(function(App) {
    'use strict';

    var routeIs = function(route, $location) {
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

    var getDefaultParamValues = function(module) {
        if (!module.examples) {
            return {};
        }
        var defaultExample = module.examples.filter(function(example) {
            return example.name.toLocaleLowerCase() === 'default';
        });
        var params = defaultExample.length ? defaultExample[0].params : module.examples[0].params;
        if (!params) {
            return {};
        }
        return params.reduce(function(acc, param) {
            var modParam = module.params.filter(function(p) {
                return p.name === param.name;
            });
            if (modParam.length && (modParam[0].type === 'Object' || modParam[0].type === 'Array')) {
                acc[param.name] = JSON.stringify(param.value);
                return acc
            }
            acc[param.name] = param.value;
            return acc;
        }, {});
    };

    var moduleDescribeToJSON = function(module, RPCParamParser) {
        var params = module.params.map(function(param) {
            return [param.name, RPCParamParser.getValue(param, true)];
        });

        return JSON.stringify(Object.fromEntries(
            new Map(params),
        ), null, 2);
    };

    var JSONToModuleDescribe = function(jsonInput, module) {
        var inputObj = {};
        try {
            inputObj = JSON.parse(jsonInput);
        } catch (e) {
            console.error('Failed to parse JSON input:', jsonInput);
            return module;
        }

        for (var i = 0; i < module.params.length; i++) {
            var param = module.params[i];
            if (param.name in inputObj) {
                if (param.type === 'Object' || param.type === 'Array') {
                    param.value = JSON.stringify(inputObj[param.name]);
                    continue;
                }
                param.value = inputObj[param.name];
            }
        }
        return module;
    };

    App.controller('ApplicationCtrl', ['$scope', '$location', '$timeout',
                                       'responseExample', 'responseObjectExample', 'PendingRequests',
                                       function($scope, $location, $timeout,
                                                responseExample, responseObjectExample, PendingRequests) {
        $scope.showFakeIntro = true;
        $scope.showContentLoaded = true;
        $scope.showToolbar = false;
        $scope.showToolbarPlayButton = true;
        $scope.showToolbarRerunButton = false;
        $scope.showToolbarNotifyButton = true;
        $scope.response = responseExample;
        $scope.responseObject = responseObjectExample;

        $scope.$on('App:displayFakeIntro', function(event, display) {
            $scope.showFakeIntro = display;
        });

        $scope.$on('App:displayContentLoaded', function(event, display) {
            $scope.showContentLoaded = display;
        });

        $scope.$on('App:displayToolbar', function(event, display) {
            $scope.showToolbar = display;
        });

        $scope.$on('App:displayToolbarNotifyButton', function(event, display) {
            $scope.showToolbarNotifyButton = display;
        });

        $scope.$on('App:route:changed', function(event, route) {
            $scope.showToolbarPlayButton = true;
            $scope.showToolbarRerunButton = false;
        });

        $scope.$on('RPC:called', function(event, responseObject) {
            $scope.showToolbarPlayButton = false;
            $scope.showToolbarRerunButton = true;
        });

        $scope.showSpinner = function() {
            return PendingRequests.isPending();
        };

        $scope.routeIs = function(route) {
            return routeIs(route, $location);
        };
    }]);

    App.controller('MenuCtrl', ['$scope', '$location', '$timeout', 'Handlebars', 'Api',
                                function($scope, $location, $timeout, Handlebars, Api) {
        $scope.$emit('App:displayFakeIntro', true);
        $scope.$emit('App:displayContentLoaded', true);
        Api.packages(function(packages) {
            $scope.packages = packages;
            $scope.$emit('App:displayFakeIntro', false);
            $timeout(function() {
                $scope.$emit('App:displayContentLoaded', false);
            }, 750);
        });

        $scope.routeIs = function(route) {
            return routeIs(route, $location);
        };

        $scope.goToDashboard = function() {
            $scope.$emit('App:displayToolbar', false);
            $location.path('/');
        };

        $scope.showTooltip = function(module) {
            return Handlebars.template('menu-module-tooltip', module);
        };

        $scope.goToModule = function(module) {
            $scope.$emit('App:route:changed', module.name);
            return $location.path(module.name);
        };
    }]);

    App.controller('ViewerContainerCtrl', ['$scope', function($scope) {
        $scope.play = function() {
            $scope.$broadcast('RPC:play');
        };

        $scope.rerun = function() {
            $scope.$broadcast('RPC:rerun');
        };

        $scope.changeParameters = function() {
            $scope.$broadcast('RPC:changeParameters');
        };

        $scope.notify = function() {
            $scope.$broadcast('RPC:notify');
        };
    }]);

    App.controller('ModuleDialogCtrl', ['$scope', '$modalInstance', 'RPCParamParser', 'module', 'options',
                                        function($scope, $modalInstance, RPCParamParser, module, options) {
        $scope.module = module;
        $scope.options = options;
        $scope.defaultParamValues = getDefaultParamValues(module);
        $scope.rawInput = moduleDescribeToJSON(module, RPCParamParser);

        // Initialize parameter values with defaults if not set
        if (options.defaultValues) {
            $scope.module.params.forEach(function(param) {
                if (param.value === undefined || param.value === null) {
                    param.value = $scope.defaultParamValues[param.name];
                }
            });
        }

        $scope.handleRawInputChange = function(newValue, oldValue) {
            if (newValue !== oldValue) {
                $scope.module = JSONToModuleDescribe(newValue, $scope.module);
            }
        }

        $scope.onInputModeChange = function() {
            if ($scope.options.inputMode === 'raw') {
                $scope.rawInput = moduleDescribeToJSON($scope.module, RPCParamParser);
            }
        };

        $scope.ok = function() {
            $modalInstance.close($scope.module);
            $scope.onInputModeChange();
        };

        $scope.hitEnter = function(evt) {
            if (angular.equals(evt.keyCode, 13) && !(angular.equals($scope.name, null) || angular.equals($scope.name, ''))) {
                $scope.ok();
            }
        };

        $scope.cancel = function() {
            $modalInstance.dismiss('cancel');
        };
    }]);

    App.controller('ResponseObjectCtrl', ['$scope', '$window', '$modal', 'RPC', 'RPCParamParser', 'module',
                                          function($scope, $window, $modal, RPC, RPCParamParser, module) {
        $scope.module = module;
        $scope.requestObject = undefined;
        $scope.response = undefined;
        $scope.responseObject = undefined;
        $scope.$emit('App:displayToolbar', true);
        $scope.$emit('App:displayToolbarNotifyButton', module.notification);

        var RPCCall = function(module) {
            var payload = RPC.payload(module);
            $scope.requestObject = payload;
            $scope.response = undefined;
            $scope.responseObject = undefined;
            RPC.callWithPayload(payload).success(function(responseObject, status, headers, config) { // success
                var headersPretty = headers();
                headersPretty.data = config.data;

                $scope.response = {status: status, headers: headersPretty, config: config};
                $scope.responseObject = responseObject;
                $scope.$emit('App:displayContentLoaded', false);
                $scope.$emit('RPC:called', responseObject);
            }).error(function(responseObject, status, headers, config) { // error
                var headersPretty = headers();
                headersPretty.data = config.data;

                $scope.response = {statusCode: status, headers: headersPretty, config: config};
                $scope.responseObject = responseObject;
                $scope.$emit('App:displayContentLoaded', false);
                $scope.$emit('RPC:called', responseObject);
            });
        },
        RPCCallModal = function(module, options = {}) {
            $modal.open({
                templateUrl: 'module_dialog.html',
                controller: 'ModuleDialogCtrl',
                resolve: {
                    RPCParamParser: function() {
                        return RPCParamParser;
                    },
                    module: function() {
                        return module;
                    },
                    options: function() {
                        return {...{
                            defaultValues: true,
                            inputMode: $scope.inputMode || 'formData',
                        }, ...options};
                    }
                }
            }).result.then(function(module) { // ok
                return RPCCall(module);
            }, function() { // cancel
                $scope.$emit('App:displayContentLoaded', false);
            });
        };

        $scope.showRequestResponsePanel = function() {
            return $scope.requestObject !== undefined && $scope.response !== undefined && $scope.responseObject !== undefined;
        };

        $scope.closeRequestResponsePanel = function() {
            $scope.requestObject = undefined;
            $scope.response = undefined;
            $scope.responseObject = undefined;
        };

        $scope.$on('RPC:play', function(event) {
            return RPCCallModal($scope.module);
        });

        $scope.$on('RPC:rerun', function(event) {
            return RPCCall($scope.module);
        });

        $scope.$on('RPC:changeParameters', function(event) {
            return RPCCallModal($scope.module, {defaultValues: false});
        });

        $scope.$on('RPC:notify', function(event) {
            var m = angular.copy($scope.module);
            m.notify = true;
            return RPCCall(m);
        });
    }]);

})(window.App);
