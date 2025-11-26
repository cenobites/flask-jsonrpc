(function(App) {
	'use strict';

	angular.module('browse.filter', [])
        .filter('prettyprint', ['$sce', function($sce) {
            return function(input) {
                try {
                    return $sce.trustAsHtml(prettyPrintOne(input));
                } catch (e) {
                    console.error('Error in prettyprint filter:', input, e);
                    return $sce.trustAsHtml(input);
                }
            };
        }])
        .filter('markdown', ['Marked', '$sce', function(Marked, $sce) {
            return function(input) {
                try {
                    return $sce.trustAsHtml(Marked.toHtml(input));
                } catch (e) {
                    console.error('Error in markdown filter:', input, e);
                    return $sce.trustAsHtml(input);
                }
            };
        }]);

})(window.App);
