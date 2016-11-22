/**
 * Created by Hernan on 21/11/2016.
 */
angular.module("materialAdmin")
    .directive('exportStep', function() {
        return {
            restrict: "E",
            templateUrl: "template/directives/export-step.html",
            controller: function ($scope) {
                $scope.classification['title'] = 'Export';
            }
        }
    });