/**
 * Created by Hernan on 11/19/2016.
 */
angular.module("materialAdmin")
    .directive('checkboxInput', function() {
        return {
            restrict: "E",
            scope: true,
            templateUrl: "template/directives/dynamic-inputs/checkbox-input.html"
        }
    });