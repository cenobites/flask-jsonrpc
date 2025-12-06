(function(App) {
	'use strict';

    var getCookie = function(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) {
            return parts.pop().split(';').shift();
        }
    };

    angular.module('rpcdescribe.service', [])
        .factory('AuthService', ['$http', '$q', function($http, $q) {

            var refreshing = false;

            // Called when token expired
            return {
                refreshToken: function() {
                    if (refreshing) {
                        // another refresh is already in progress → return its promise
                        return refreshing;
                    }

                    var refreshToken = localStorage.getItem('refresh_token');
                    if (!refreshToken) {
                        return $q.reject("no refresh token");
                    }

                    var deferred = $q.defer();
                    refreshing = deferred.promise;

                    $http.post('/oauth/token/refresh', {}, {
                            headers: {
                                'Content-Type': 'application/json',
                                'Authorization': `Bearer ${localStorage.getItem('refresh_token')}`
                            }
                        })
                        .then(function(res) {
                            var newToken = res.data.access_token;

                            localStorage.setItem('jwt', newToken);

                            deferred.resolve(newToken);
                            refreshing = false;
                        }, function(err) {
                            deferred.reject(err);
                            refreshing = false;
                        });

                    return deferred.promise;
                }
            };
        }])
        .factory('Oauth2HttpInterceptor', ['$q', '$injector', function($q, $injector) {
            return {
                // Intercept outgoing requests
                request: function(config) {
                    if (config.url.startsWith('/api')) {
                        // Example: add auth header
                        if (localStorage.getItem('jwt')) {
                            config.headers['Authorization'] = `Bearer ${localStorage.getItem('jwt')}`;
                        }

                        var csrfToken = getCookie('csrf_access_token');
                        if (csrfToken) {
                            config.headers['X-CSRF-TOKEN'] = csrfToken;
                        }
                    }
                    return config;
                },

                // Intercept request errors
                requestError: function(rejection) {
                    return $q.reject(rejection);
                },

                // Intercept incoming responses
                response: function(response) {
                    return response;
                },

                // Intercept response errors
                responseError: function(rejection) {
                    // return $q.reject(rejection);
                    if (rejection.status !== 401) {
                        return $q.reject(rejection);
                    }

                    var $http = $injector.get('$http');
                    var originalRequest = rejection.config;

                    // Avoid infinite retry loops
                    if (originalRequest._retry) {
                        return $q.reject(rejection);
                    }
                    originalRequest._retry = true;

                    // Wait for token refresh
                    var AuthService = $injector.get('AuthService');
                    return AuthService.refreshToken().then(function(newToken) {

                        // Update Authorization header
                        originalRequest.headers.Authorization = 'Bearer ' + newToken;

                        // Retry original request
                        return $http(originalRequest);

                        },
                        function(err) {
                            return $q.reject(err);
                        }
                    );
                }
            };
        }])
        .config(['$httpProvider', function($httpProvider) {
            $httpProvider.interceptors.push('Oauth2HttpInterceptor');
        }]);

    // Register the service module with the main application
    App.requires.push('rpcdescribe.service');

})(window.App);
