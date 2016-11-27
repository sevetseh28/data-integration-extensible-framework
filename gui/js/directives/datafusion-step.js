/**
 * Created by Hernan on 21/11/2016.
 */
angular.module("materialAdmin")
    .directive('datafusionStep', function() {
        return {
            restrict: "E",
            templateUrl: "template/directives/datafusion-step.html",
            controller: function ($scope) {
                $scope.datafusion['title'] = 'Data Fusion';

                $scope.datafusion.returnValue = {
                    selected_module: {
                        name: '',
                        config: {}
                    }
                };

                $scope.$watch('datafusion.selectedModule', function(){
                    $scope.datafusion.returnValue.selected_module.name = $scope.datafusion.selectedModule.id;
                }, true);
            }
        }
    });