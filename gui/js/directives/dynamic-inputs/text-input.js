angular.module("materialAdmin")
.directive('textInput', function() {
    return {
        restrict: "E",
        scope: true,
        templateUrl: "template/directives/dynamic-inputs/text-input.html"
    }
});