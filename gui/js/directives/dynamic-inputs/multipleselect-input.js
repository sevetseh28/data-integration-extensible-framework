angular.module("materialAdmin")
    .directive('multipleselectInput', function () {
        return {
            restrict: "E",
            scope: true,
            templateUrl: "template/directives/dynamic-inputs/multipleselect-input.html",
            link: function (scope, element, attrs) {

                function appendReturnValue() {
                    scope.returnValue[scope.configId] = scope.config.selectedoption;

                    if ('nestedCheck' in scope) {
                        scope.nestedCheck['check'] ++
                    }
                }

                scope.$watch('config', appendReturnValue, true);

            }
        }
    });