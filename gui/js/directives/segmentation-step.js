angular.module("materialAdmin")
    .directive('segmentationStep', function () {
        return {
            restrict: "E",
            templateUrl: "template/directives/segmentation-step.html",
            controller: function ($scope) {

                $scope.segmentation['title'] = 'Segmentation';

                $scope.segmentation.returnValue = {
                    selected_module: {
                        name: '',
                        config: {}
                    }
                };

                $scope.$watch('segmentation.selectedModule', function(){
                    $scope.segmentation.returnValue.selected_module.name = $scope.segmentation.selectedModule.id;
                }, true);
            }
        }
    });