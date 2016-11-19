angular.module("materialAdmin")
.directive('multipleselectInput', function() {
    return {
        restrict: "E",
        scope: true,
        templateUrl: "template/directives/dynamic-inputs/multipleselect-input.html"
    }
});