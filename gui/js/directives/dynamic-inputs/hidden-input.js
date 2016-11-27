angular.module("materialAdmin")
    .directive('hiddenInput', function () {
        return {
            restrict: "E",
            scope: true,
            templateUrl: "template/directives/dynamic-inputs/hidden-input.html",
            link: function (scope, element, attrs) {

                function appendReturnValue() {
                    scope.returnValue[scope.configId] = scope.config.value;

                    if ('nestedCheck' in scope) {
                        scope.nestedCheck['check'] ++
                    }
                }

                scope.$watch('config', appendReturnValue, true);

            }

        }
    });