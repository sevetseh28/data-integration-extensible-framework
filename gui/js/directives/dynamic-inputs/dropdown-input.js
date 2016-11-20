/**
 * Created by Hernan on 20/11/2016.
 */
angular.module("materialAdmin")
    .directive('dropdownInput', function() {
        return {
            restrict: "E",
            scope: true,
            templateUrl: "template/directives/dynamic-inputs/dropdown-input.html"

        }
    });