angular.module("materialAdmin")
.directive('rowsInput', function() {
    return {
        restrict: "E",
        scope: true,
        templateUrl: "template/directives/dynamic-inputs/rows-input.html",
        link: function(scope, element, attrs) {
        },
        controller: function ($scope) {
            $scope.addRow = function () {
                $scope.config.rows.push(angular.copy($scope.config.rowmodel));
            };

            $scope.removeRow = function (index) {
                $scope.config.rows.splice(index, 1)
            };

        }
    }
});