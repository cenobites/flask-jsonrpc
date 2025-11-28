(function(App) {
	'use strict';

	angular.module('core.directive', [])
        .directive('disableable', ['$parse', function($parse) {
            return {
                restrict: 'C',
                require: '?ngClick',
                link: function (scope, elem, attrs, ngClick) {
                    elem.bind('click', function (e) {
                        e.stopImmediatePropagation();
                        return false;
                    });

                 }
             };
        }])
        .directive('codeMirror', [function() {
            return {
                restrict: 'E',
                require: 'ngModel',
                scope: {
                    ngModel: '=',
                    onChange: '&onChange'
                },
                link: function(scope, element, attrs, ngModelCtrl) {
                    var cursorPosition = { line: 0, ch: 0 };
                    var editor = CodeMirror(element[0], {
                        value: scope.ngModel || '',
                        mode: 'application/json',
                        lineNumbers: true,
                        theme: 'default',
                        matchBrackets: true
                    });

                    editor.on('change', function() {
                        if (editor.getValue() !== scope.ngModel) {
                            scope.$apply(function () {
                                try {
                                    JSON.parse(editor.getValue());
                                    if (scope.onChange) {
                                        scope.onChange({newValue: editor.getValue(), oldValue: scope.ngModel});
                                    }
                                } catch (e) {
                                    // Ignore JSON parse errors
                                } finally {
                                    ngModelCtrl.$setViewValue(editor.getValue());
                                }
                            });
                        }
                    });

                    scope.$watch('ngModel', function(newValue, oldValue) {
                        if (editor && newValue !== oldValue) {
                            cursorPosition = editor.getCursor();
                            editor.setValue(newValue || '');
                            if (oldValue !== '') {
                                editor.setCursor(cursorPosition);
                            }
                        }
                    });
                }
            };
        }]);

})(window.App);
