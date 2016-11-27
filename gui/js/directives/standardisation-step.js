angular.module("materialAdmin")
    .directive('standardisationStep', function () {
        return {
            restrict: "E",
            templateUrl: "template/directives/standardisation-step.html",
            controller: function ($scope) {
                $scope.standardisation['title'] = 'Standardisation';


                // SELECCIONES DE MODULOS
                $scope.standardisation['addOption'] = function (source) {
                    $scope.standardisation['moduleSelections'][source].push(angular.copy($scope.standardisation['modules']))
                };

                $scope.standardisation['removeOption'] = function (index, source) {
                    $scope.standardisation['moduleSelections'][source].splice(index, 1)
                };


                $scope.standardisation['moduleSelections'] = {};

                $scope.standardisation.empty = {};

                $scope.standardisation.updateReturnValue = function() {
                    $scope.standardisation.returnValue = {
                        source1: {},
                        source2: {}
                    };

                    var source_configs;
                    for (var source in $scope.sources) {
                        source = $scope.sources[source];
                        source_configs = $scope.standardisation.returnValue[source];
                        module_selections = $scope.standardisation['moduleSelections'][source];
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

                $scope.$watch('standardisation.moduleSelections', $scope.standardisation.updateReturnValue, true);

                $scope.standardisation['moduleSelections']['source1'] = [];
                $scope.standardisation['moduleSelections']['source2'] = []
            }
        }
    });