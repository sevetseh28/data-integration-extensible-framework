/**
 * Created by Hernan on 21/11/2016.
 */
angular.module("materialAdmin")
    .directive('exportStep', function() {
        return {
            restrict: "E",
            templateUrl: "template/directives/export-step.html",
            controller: function ($scope) {
                $scope.export['title'] = 'Export';

                $scope.export.returnValue = {
                    selected_module: {
                        name: '',
                        config: {}
                    }
                };

                $scope.$watch('export.selectedModule', function(){
                    $scope.export.returnValue.selected_module.name = $scope.export.selectedModule.id;
                }, true);
            }
        }
    });