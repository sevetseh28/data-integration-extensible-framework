angular.module("materialAdmin")
    .directive('standardisationStep', function () {
        return {
            restrict: "E",
            templateUrl: "template/directives/standardisation-step.html",
            controller: function ($scope) {
                $scope.standardisation['title'] = 'Standardisation';

                // SE INICIALIZAN LAS COLUMNAS PARA CADA source
                // en principio esta hardcodeado pero aca se debe llamar al servicio para ver cuales hay
                $scope.standardisation['columns'] = {
                    'source1': [
                        {
                            name: 'Apellido'
                        },
                        {
                            name: 'Nombre'
                        },
                        {
                            name: 'Telefono'
                        }
                    ],
                    'source2': [
                        {
                            name: 'Nombre y apellido'
                        },
                        {
                            name: 'Direccion'
                        }
                    ]
                }


                // SELECCIONES DE MODULOS
                $scope.standardisation['addOption'] = function (source) {
                    $scope.standardisation['moduleSelections'][source].push(angular.copy($scope.standardisation['modules']))
                }

                $scope.standardisation['removeOption'] = function (index, source) {
                    $scope.standardisation['moduleSelections'][source].splice(index, 1)
                }


                $scope.standardisation['moduleSelections'] = {}

                $scope.standardisation['moduleSelections']['source1'] = []
                $scope.standardisation['moduleSelections']['source2'] = []
            }
        }
    });