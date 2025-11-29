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
        }]);
})(window.App);
