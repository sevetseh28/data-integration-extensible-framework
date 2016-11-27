angular.module("materialAdmin")
    .directive('schemamatchingStep', function () {
        return {
            restrict: "E",
            templateUrl: "template/directives/schemamatching-step.html",
            controller: function ($scope) {
                $scope.schemamatching['title'] = 'Schema Matching';

                $scope.schemamatching.returnValue = {
                    selected_module: {
                        name: '',
                        config: {}
                    }
                };

                $scope.$watch('schemamatching.selectedModule', function(){
                    $scope.schemamatching.returnValue.selected_module.name = $scope.schemamatching.selectedModule.id;
                }, true);
            }
        }
    });