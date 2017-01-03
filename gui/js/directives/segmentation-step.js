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
                    selected_module: {
                        name: '',
                        config: {}
                    },
                    skipstep: false
                };
                $scope.segmentation.toggleskip = {
                    config: {
                        label: 'Skip this step (output fields will not be used)',
                        color: "red"
                    }
                };
                $scope.segmentation.skiptoggler = function() {
                    $scope.segmentation.returnValue.skipstep = !($scope.segmentation.returnValue.skipstep)
                };

                $scope.segmentation.updateReturnValue = function() {
                    $scope.segmentation.returnValue = {
                        source1: {},
                        source2: {}
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
            }
        }
    });