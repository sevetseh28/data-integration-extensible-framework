/**
 * Created by Hernan on 31/12/2016.
 */
angular.module("materialAdmin")
    .directive('standardisationtaggingStep', function () {
        return {
            restrict: "E",
            templateUrl: "template/directives/standardisationtagging-step.html",
            controller: function ($scope) {
                $scope.standardisationtagging['title'] = 'Standardisation and tagging';

                $scope.standardisationtagging['moduleSelections'] = {};
                $scope.standardisationtagging['moduleSelections']['source1'] = [];
                $scope.standardisationtagging['moduleSelections']['source2'] = [];



                $scope.standardisationtagging.empty = {};

                $scope.standardisationtagging.updateReturnValue = function() {
                    $scope.standardisationtagging.returnValue = {
                        source1: {},
                        source2: {}
                    };

                    var source_configs;
                    for (var source in $scope.sources) {
                        source = $scope.sources[source];
                        source_configs = $scope.standardisationtagging.returnValue[source];
                        module_selections = $scope.standardisationtagging['moduleSelections'][source];
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

                $scope.$watch('standardisationtagging.moduleSelections', $scope.standardisationtagging.updateReturnValue, true);
            }
        }
    });