/**
 * Created by Hernan on 21/11/2016.
 */
angular.module("materialAdmin")
    .directive('datafusionStep', function() {
        return {
            restrict: "E",
            templateUrl: "template/directives/datafusion-step.html",
            controller: function ($scope) {
                $scope.classification['title'] = 'Data Fusion';
            }
        }
    });