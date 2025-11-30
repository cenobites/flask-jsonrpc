(function(App) {
	'use strict';

	angular.module('browse.directive', [])
        .directive('__prettyprint-it', [function() {
            return {
                restrict: 'C',
                link: function postLink(scope, element, attrs) {
                    return element.html(prettyPrintOne('{}'));
                }
            };
        }])
        .directive('menuTree', ['urlPrefix', function(urlPrefix) {
            return {
                restrict: 'E',
                scope: {
                    node: '=',
                    onClick: '&',
                },
                templateUrl: urlPrefix + '/partials/menu_tree.html',
                controller: ['$scope', 'urlPrefix', function ($scope, urlPrefix) {
                    $scope.urlPrefix = urlPrefix;
                    $scope.routeIs = $scope.$parent.routeIs;
                    $scope.showTooltip = $scope.$parent.showTooltip;
                    $scope.select = function (item) {
                        if ($scope.onClick) {
                            $scope.onClick({item: item});
                        }
                    };
                }]
            };
        }])
        .directive('fieldDescribe', ['urlPrefix', function(urlPrefix) {
            return {
                restrict: 'E',
                scope: {
                    field: '=',
                    level: '@'
                },
                templateUrl: urlPrefix + '/partials/field_describe.html',
                controller: ['$scope', 'urlPrefix', function ($scope, urlPrefix) {
                    $scope.level = $scope.level || 0;
                    $scope.urlPrefix = urlPrefix;

                    $scope.hasConstraints = function(field) {
                        return field.minimum !== null && field.minimum !== undefined ||
                            field.maximum !== null && field.maximum !== undefined ||
                            field.multiple_of !== null && field.multiple_of !== undefined ||
                            field.min_length !== null && field.min_length !== undefined ||
                            field.max_length !== null && field.max_length !== undefined ||
                            field.pattern ||
                            field.max_digits !== null && field.max_digits !== undefined ||
                            field.decimal_places !== null && field.decimal_places !== undefined;
                    };
                }]
            };
        }])
        .directive('exampleDescribe', [function() {
            return {
                restrict: 'E',
                scope: {
                    example: '='
                },
                template: `
                    <div class="example-doc panel panel-default">
                        <div class="panel-heading">
                            <h4>
                                <span ng-if="example.name">{{example.name}}</span>
                                <span ng-if="!example.name">Example</span>
                                <small ng-if="example.summary"> - {{example.summary}}</small>
                            </h4>
                        </div>
                        <div class="panel-body">
                            <p ng-if="example.description" ng-bind-html="example.description|markdown"></p>

                            <div ng-if="example.params && example.params.length">
                                <h5>Parameters:</h5>
                                <pre>{{getParamsJSON(example.params)}}</pre>
                            </div>

                            <div ng-if="example.returns">
                                <h5>Returns:</h5>
                                <pre>{{example.returns.value | json}}</pre>
                                <p ng-if="example.returns.description" class="text-muted">
                                    {{example.returns.description}}
                                </p>
                            </div>
                        </div>
                    </div>
                `,
                link: function(scope) {
                    scope.getParamsJSON = function(params) {
                        var obj = {};
                        params.forEach(function(p) {
                            obj[p.name] = p.value;
                        });
                        return JSON.stringify(obj, null, 2);
                    };
                }
            };
        }]);
})(window.App);
