angular.module("materialAdmin")
.directive('rowInput', function() {
    return {
        restrict: "E",
        scope: true,
        templateUrl: "template/directives/dynamic-inputs/row-input.html"
    }
});