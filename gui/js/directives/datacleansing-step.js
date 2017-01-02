angular.module("materialAdmin")
    .directive('datacleansingStep', function () {
        return {
            restrict: "E",
            templateUrl: "template/directives/datacleansing-step.html",
            controller: function ($scope) {
                $scope.datacleansing['title'] = 'Data Cleansing';


                // SELECCIONES DE MODULOS
                $scope.datacleansing['addOption'] = function (source) {
                    $scope.datacleansing['moduleSelections'][source].push(angular.copy($scope.datacleansing['modules']))
                };

                $scope.datacleansing['removeOption'] = function (index, source) {
                    $scope.datacleansing['moduleSelections'][source].splice(index, 1)
                };


                $scope.datacleansing['moduleSelections'] = {};

                $scope.datacleansing.empty = {};

                $scope.datacleansing.updateReturnValue = function() {
                    $scope.datacleansing.returnValue = {
                        source1: {},
                        source2: {}
                    };

                    var source_configs;
                    for (var source in $scope.sources) {
                        source = $scope.sources[source];
                        source_configs = $scope.datacleansing.returnValue[source];
                        module_selections = $scope.datacleansing['moduleSelections'][source];
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
                                if(module.moduleSelected.config[config].returnValue)
                                    retVal.config[config] = module.moduleSelected.config[config].returnValue[config]
                            }
                            source_configs[module.columnSelected].push(retVal)
                        }
                    }
                }

                $scope.$watch('datacleansing.moduleSelections', $scope.datacleansing.updateReturnValue, true);

                $scope.datacleansing['moduleSelections']['source1'] = [];
                $scope.datacleansing['moduleSelections']['source2'] = []
            }
        }
    });