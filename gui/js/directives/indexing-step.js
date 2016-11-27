/**
 * Created by Hernan on 20/11/2016.
 */
angular.module("materialAdmin")
    .directive('indexingStep', function () {
        return {
            restrict: "E",
            templateUrl: "template/directives/indexing-step.html",
            controller: function ($scope) {
                $scope.indexing['title'] = 'Indexing';
                
                $scope.indexing.returnValue = {
                    selected_module: {
                        name: '',
                        config: {}
                    }
                };

                $scope.$watch('indexing.selectedModule', function(){
                    $scope.indexing.returnValue.selected_module.name = $scope.indexing.selectedModule.id;
                }, true);

            }
        }
    });