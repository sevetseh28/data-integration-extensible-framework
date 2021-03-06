angular.module("materialAdmin")
    .directive('rowsInput', function () {
        return {
            restrict: "E",
            scope: true,
            templateUrl: "template/directives/dynamic-inputs/rows-input.html",
            link: function (scope, element, attrs, $timeout) {

                scope.childReturnValues = [];
                scope.nestedChecks = {};

                scope.loadChildControl = function (k) {
                    scope.childReturnValues[k] = {};
                };

                scope.loadNestedCheck = function (k) {
                    scope.nestedChecks[k] = {'check':0};
                };

                scope.initControls = function(k){
                    scope.loadChildControl(k);
                    scope.loadNestedCheck(k);
                };

                scope.appendReturnValue = function() {
                    var ret = [];

                    for (var row in scope.childReturnValues) {
                        ret[row] = scope.childReturnValues[row][scope.configId]
                    }

                    scope.returnValue[scope.configId] = ret
                };

                scope.$watch(function(){return scope.nestedChecks}, scope.appendReturnValue, true);

            },
            controller: function ($scope) {
                $scope.addRow = function () {
                    $scope.config.rows.push(angular.copy($scope.config.rowmodel));
                };

                $scope.removeRow = function (index) {
                    $scope.config.rows.splice(index, 1);
                    $scope.childReturnValues.splice(index, 1);
                    $scope.appendReturnValue()
                };

            }
        }
    });