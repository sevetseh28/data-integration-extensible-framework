angular.module("materialAdmin")
    .directive('radioInput', function() {
        return {
            restrict: "E",
            scope: true,
            templateUrl: "template/directives/dynamic-inputs/radio-input.html"
        }
    });