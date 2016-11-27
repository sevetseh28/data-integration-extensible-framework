angular.module("materialAdmin")
    .directive('radioInput', function() {
        return {
            restrict: "E",
            scope: true,
            templateUrl: "template/directives/dynamic-inputs/radio-input.html",
            link: function (scope, element, attrs) {

                function appendReturnValue() {
                    scope.returnValue[scope.configId] = scope.config.selected;

                    if ('nestedCheck' in scope) {
                        scope.nestedCheck['check'] ++
                    }
                }

                scope.$watch('config', appendReturnValue, true);

            }
        }
    });