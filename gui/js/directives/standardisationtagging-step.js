/**
 * Created by Hernan on 31/12/2016.
 */
angular.module("materialAdmin")
    .directive('standardisationtaggingStep', function () {
        return {
            restrict: "E",
            templateUrl: "template/directives/standardisationtagging-step.html",
            controller: function ($scope) {
                $scope.datacleansing['title'] = 'Standardisation and tagging';


                // SELECCIONES DE MODULOS
                $scope.standardisationtagging['addOption'] = function (source) {
                    $scope.standardisationtagging['moduleSelections'][source].push(angular.copy($scope.datacleansing['modules']))
                };

                $scope.standardisationtagging['removeOption'] = function (index, source) {
                    $scope.standardisationtagging['moduleSelections'][source].splice(index, 1)
                };


                $scope.standardisationtagging['moduleSelections']['source1'] = {};
                $scope.standardisationtagging['moduleSelections']['source2'] = {};

                for (var i = 0; i < $scope.standardisationtagging['columns']['source1'].length; i++) {
                    $scope.standardisationtagging['moduleSelections']['source1']
                        .push(angular.copy($scope.datacleansing['modules']));
                    var selectedColumn = {
                        'columnSelected': $scope.standardisationtagging['columns']['source1'][i]
                    };
                    $scope.standardisationtagging['moduleSelections']['source1']
                        .push(selectedColumn);
                }

                for (var i = 0; i < $scope.standardisationtagging['columns']['source2'].length; i++) {
                    $scope.standardisationtagging['moduleSelections']['source2']
                        .push(angular.copy($scope.datacleansing['modules']));
                    var selectedColumn = {
                        'columnSelected': $scope.standardisationtagging['columns']['source1'][i]
                    };
                    $scope.standardisationtagging['moduleSelections']['source2']
                        .push(selectedColumn);
                }

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
                        for (var module in module_selections) {
                            module = module_selections[module];
                            if (!module.columnSelected || !module.moduleSelected)
                                continue;
                            if (!(module.columnSelected in source_configs)) {
                                source_configs[module.columnSelected] = []
                            }
                            retVal = {
                                    name: module.moduleSelected.id,
                                    config:{}
                            };
                            for (var config in module.moduleSelected.config) {
                                retVal.config[config] = module.moduleSelected.config[config].returnValue[config]
                            }
                            source_configs[module.columnSelected].push(retVal)
                        }
                    }
                }

                $scope.$watch('standardisationtagging.moduleSelections', $scope.standardisationtagging.updateReturnValue, true);

                $scope.datacleansing['moduleSelections']['source1'] = [];
                $scope.datacleansing['moduleSelections']['source2'] = []
            }
        }
    });