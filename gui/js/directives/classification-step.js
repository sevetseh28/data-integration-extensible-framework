/**
 * Created by Hernan on 21/11/2016.
 */
angular.module("materialAdmin")
    .directive('classificationStep', function() {
        return {
            restrict: "E",
            templateUrl: "template/directives/classification-step.html",
            controller: function ($scope) {
                $scope.classification['title'] = 'Classification';
            }
        }
    });