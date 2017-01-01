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
                    },
                    skipstep: false,
                };
                $scope.segmentation.toggleskip = {
                    config: {
                        label: 'Skip this step and don\'t use output fields',
                        color: "red",
                    }
                };
                $scope.segmentation.skiptoggler = function() {
                    $scope.segmentation.returnValue.skipstep = !($scope.segmentation.returnValue.skipstep)
                };

                $scope.$watch('segmentation.selectedModule', function(){
                    $scope.segmentation.returnValue.selected_module.name = $scope.segmentation.selectedModule.id;
                }, true);
            }
        }
    });