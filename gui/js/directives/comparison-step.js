/**
 * Created by Hernan on 20/11/2016.
 */
angular.module("materialAdmin")
    .directive('comparisonStep', function () {
        return {
            restrict: "E",
            templateUrl: "template/directives/comparison-step.html",
            controller: function ($scope) {
                $scope.comparison['title'] = 'Comparison';

            }
        }
    });