(function(root) {
	'use strict';

	var App = angular.module('browse', ['ngRoute', 'ngResource', 'ui.bootstrap',
		'core.service', 'core.directive', 'core.filter', 
		'browse.service', 'browse.directive', 'browse.filter'
		]).
		config(['$routeProvider', function($routeProvider) {
	    	$routeProvider
	    		.when('/', {
	    			reloadOnSearch: false,
	    			templateUrl: '/browse/partials/dashboard.html',
                    controller: 'ApplicationCtrl',
                    resolve: {
                        packages: ['ContentLoaded', 'Api', function(ContentLoaded, Api) {
                            ContentLoaded.show();
                            //return Api.packages().$promise;
                            return [];
                        }]
                    }
	    		})
                .when('/:method', {
                    controller: 'ResponseObjectCtrl',
                    templateUrl: '/browse/partials/response_object.html',
                    resolve: {
                        module: ['$route', 'ContentLoaded', 'Api', function($route, ContentLoaded, Api) {
                            ContentLoaded.show();
                            return Api.method({service: $route.current.params.method}).$promise;
                        }]
                    }
                })
	    		.otherwise({
	    			redirectTo: '/'
	    		});
		}]);

	App.adjust = function() {
        var viewPortHeight = $(window).outerHeight(true),
            viewPortWidth = $(window).outerWidth(true),
            viewPortMenu = viewPortHeight - $('#navbar-main').outerHeight(true) - $('#logo-section').outerHeight(true) - $('#box-subscribe').outerHeight(true),
            viewPortContent = viewPortHeight - $('#navbar-main').outerHeight(true) - $('#viewer-header-container').outerHeight(true),
            viewPortIframe = viewPortContent - $('#title-and-status-container').outerHeight(true);

        // Menu
    	$('#scrollable-sections').height(viewPortMenu);

        // Content master
    	$('#viewer-entries-container').height(viewPortContent);
    };

	App.ready = function(E) {
		// 
        $(window).bind('load resize scroll', function(env) {
            App.adjust();
        });

        //
        //$('.tooltip-it').tooltip({delay: {show: 800, hide: 100}});
	};

	root.App = App;
})(window);