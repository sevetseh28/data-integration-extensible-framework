angular.module("materialAdmin")
    .directive('segmentationStep', function () {
        return {
            restrict: "E",
            templateUrl: "template/directives/segmentation-step.html",
            controller: function ($scope) {

                $scope.segmentation['title'] = 'Segmentation';
                $scope.segmentation['moduleSelections'] = {};
                $scope.segmentation['moduleSelections']['source1'] = [];
                $scope.segmentation['moduleSelections']['source2'] = [];

                $scope.segmentation.returnValue = {
                    skipstep: false
                };
                $scope.segmentation.toggleskip = {
                    config: {
                        label: 'Skip this step (output fields will not be used)',
                        color: "red",
                        checked: false
                    }
                };
                $scope.segmentation.toggle = function() {
                     $scope.segmentation.toggleskip.config.checked = !($scope.segmentation.toggleskip.config.checked)
                };

                $scope.segmentation.updateReturnValue = function() {
                    $scope.segmentation.returnValue = {
                        source1: {},
                        source2: {},
                        skipstep: $scope.segmentation.toggleskip.config.checked
                    };

                    var source_configs;
                    for (var source in $scope.sources) {
                        source = $scope.sources[source];
                        source_configs = $scope.segmentation.returnValue[source];
                        module_selections = $scope.segmentation['moduleSelections'][source];
                        for (var module_selection_idx in module_selections) {
                            module_selection = module_selections[module_selection_idx];
                            //module = module_selections['modules'][module];
                            if (!module_selection.moduleSelected) // havent selected any module
                                continue;
                            // if (!(module_selection.columnSelected in source_configs)) {
                            //     source_configs[module.columnSelected] = []
                            // }
                            retVal = {
                                    name: module_selection.moduleSelected.id,
                                    config:{}
                            };
                            for (var config in module_selection.moduleSelected.config) {
                                retVal.config[config] = module_selection.moduleSelected.config[config].returnValue[config]
                            }
                            source_configs[module_selection.column] = retVal;
                        }
                    }
                };

                $scope.$watch('segmentation.moduleSelections', $scope.segmentation.updateReturnValue, true);
                $scope.$watch('segmentation.toggleskip', $scope.segmentation.updateReturnValue, true);
            }
        }
    });