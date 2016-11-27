angular.module("materialAdmin")
    .directive('textInput', function () {
        return {
            restrict: "E",
            scope: true,
            templateUrl: "template/directives/dynamic-inputs/text-input.html",
            link: function (scope, element, attrs) {

                function appendReturnValue() {
                    scope.returnValue[scope.configId] = scope.config.value;
                }

                scope.$watch('config', appendReturnValue, true);

            }

        }
    });