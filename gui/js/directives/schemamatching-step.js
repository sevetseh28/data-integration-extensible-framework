angular.module("materialAdmin")
    .directive('schemamatchingStep', function () {
        return {
            restrict: "E",
            templateUrl: "template/directives/schemamatching-step.html",
            controller: function ($scope) {
                $scope.schemamatching['title'] = 'Schema Matching';

            }
        }
    });