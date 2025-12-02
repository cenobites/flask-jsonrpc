(function(root) {
	'use strict';

	var App = angular.module('browse', ['ngRoute', 'ngResource', 'ngSanitize', 'ngAnimate',
        'ui.bootstrap', 'chieffancypants.loadingBar',
		'core.service', 'core.directive', 'core.filter',
		'browse.service', 'browse.directive', 'browse.filter'
	]).config(['$routeProvider', 'urlPrefix', function($routeProvider, urlPrefix) {
        $routeProvider
            .when('/', {
                reloadOnSearch: false,
                templateUrl: urlPrefix + '/partials/dashboard.html',
                controller: 'ApplicationCtrl'
            })
            .when('/:method', {
                controller: 'ResponseObjectCtrl',
                templateUrl: urlPrefix + '/partials/response_object.html',
                resolve: {
                    module: ['$route', 'Api', function($route, Api) {
                        return Api.method({service: $route.current.params.method}).$promise;
                    }]
                }
            })
            .otherwise({
                redirectTo: urlPrefix
            });
    }]);

	App.adjust = function() {
        var viewPortHeight = $(window).outerHeight(true),
            viewPortMenu = (
                viewPortHeight - ($('#navbar-main').outerHeight(true) || 0)
                    - ($('#logo-section').outerHeight(true) || 0)
                    - ($('#box-subscribe').outerHeight(true) || 0)
            ),
            viewPortContent = (
                viewPortHeight - ($('#navbar-main').outerHeight(true) || 0)
                    - ($('#viewer-header-container').outerHeight(true) || 0)
            );

        // Menu
    	$('#scrollable-sections').height(Math.max(viewPortMenu, viewPortContent));

        // Content master
    	$('#viewer-entries-container').height(Math.max(viewPortMenu, viewPortContent));
    };

	App.ready = function(E) {
		// Bind adjust on load, resize, scroll
        $(window).bind('load resize scroll', function(env) {
            App.adjust();
        });

        // JSON highlighting
        prettyPrint();

        // Initial adjust
        App.adjust();
	};

	root.App = App;
})(window);
