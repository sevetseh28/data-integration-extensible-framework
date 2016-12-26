materialAdmin

//====================================
// STEPS
//====================================

    .controller('StepsCtrl', function (APIService, $scope, $stateParams) {
        $scope.currentStep = 0;

        $scope.sources = ['source1', 'source2'];

        $scope.steps = [
            'extraction',
            'standardisation',
            'segmentation',
            'schemamatching',
            'indexing',
            'comparison',
            'classification',
            'datafusion',
            'export'
        ];

        // Esta funcion es global y es llamada por cada directiva de step para cargar los modulos disponibles
        $scope.loadStep = function (step) {

            // llamo al servicio y cargo en la variable modules de step los modulos disponibles
            if (step == 'extraction') {
                APIService.getModules($stateParams.id, step).then(function (data) {
                    $scope[step]['modules']['source1'] = data.data;
                    $scope[step]['modules']['source2'] = angular.copy($scope[step]['modules']['source1']);
                });
            } else if (step == 'standardisation') {
                APIService.getModules($stateParams.id, step).then(function (data) {
                    $scope[step]['modules'] = data.data;
                });

                APIService.getColumnsSources($stateParams.id).then(function (response) {
                    $scope.standardisation['columns'] = {
                        'source1': response.data.source1,
                        'source2': response.data.source2
                    }
                });

            } else if (step == 'segmentation') {
                APIService.getModules($stateParams.id, step).then(function (data) {
                    $scope[step]['modules'] = data.data;
                });

            } else if (step == 'schemamatching') {
                APIService.getModules($stateParams.id, step).then(function (data) {
                    $scope[step]['modules'] = data.data;
                });

            } else if (step == 'comparison') {
                APIService.getOutputFields($stateParams.id).then(function (data) {
                    $scope[step]['outputFields'] = data.data;

                    APIService.getModules($stateParams.id, step).then(function (data) {
                        $scope[step]['modules'] = data.data;
                        for (var i = 0; i < $scope[step]['outputFields'].length; i++) {
                            $scope[step]['outputFields'][i]['modules'] = angular.copy($scope[step]['modules']);
                            $scope[step]['outputFields'][i]['selectedModule'] = {'name': 'Test'};
                        }
                    });
                });

            } else if (step == 'indexing') {
                APIService.getModules($stateParams.id, step).then(function (data) {
                    $scope[step]['modules'] = data.data;
                });
            } else if (step == 'classification') {
                APIService.getModules($stateParams.id, step).then(function (data) {
                    $scope[step]['modules'] = data.data;
                });
            } else if (step == 'datafusion') {
                APIService.getModules($stateParams.id, step).then(function (data) {
                    $scope[step]['modules'] = data.data;
                });

            } else if (step == 'export') {
                APIService.getModules($stateParams.id, step).then(function (data) {
                    $scope[step]['modules'] = data.data;
                });

            }
        };

        // INICIALIZACION DE OBJETOS DE steps
        $scope.extraction = {
            selectedModules: {
                'source1': {'config': {}},
                'source2': {'config': {}}
            },
            modules: []
        };

        $scope.standardisation = {
            selectedModules: {
                'source1': [],
                'source2': []
            },
            modules: [],
            columns: {}
        };

        $scope.segmentation = {
            selectedModule: {},
            modules: []
        };

        $scope.schemamatching = {
            selectedModule: {},
            modules: []
        };

        $scope.indexing = {
            selectedModule: {},
            modules: []
        };

        $scope.comparison = {
            outputFields: [],
            modules: []
        };

        $scope.classification = {
            selectedModule: {},
            modules: []
        };

        $scope.datafusion = {
            selectedModule: {},
            modules: []
        };

        $scope.export = {
            selectedModule: {},
            modules: []
        };


        $scope.runCurrentStep = function () {
            stepId = $scope.tabs[$scope.currentStep].id;
            stepName = $scope.steps[$scope.currentStep];

            APIService.run($stateParams.id, stepId, $scope[stepName].returnValue).then(function () {
                    $scope.tabs[$scope.currentStep]['active'] = false;
                    $scope.currentStep = $scope.currentStep + 1;
                    $scope.tabs[$scope.currentStep]['disabled'] = false;

                    $scope.loadStep($scope.steps[$scope.currentStep]);

                    $scope.tabs[$scope.currentStep]['active'] = true;
                }, function (response) {
                    swal({
                            title: "An error has occured!",
                            type: "error",
                            text: 'Please check modules are selected and fully configured',
                            html: true,
                            showCancelButton: true,
                            confirmButtonText: "Ok",
                            cancelButtonText: "See details",
                            closeOnConfirm: true,
                            closeOnCancel: false
                        },
                        function (isConfirm) {
                            if (!isConfirm) {
                                swal({
                                        title: "Error details",
                                        text: '<div style="text-align: left" id="stacktrace"><small>' + response.data.details + '</small></div>',
                                        html: true
                                    }
                                );
                            }
                        });
                }
            );
        }
        ;

        $scope.tabs = [
            {
                title: 'Extract',
                directive: 'extraction-step',
                active: true,
                disabled: false,
                id: 'ExtractionStep'
            },
            {
                title: 'Standardise',
                directive: 'standardisation-step',
                active: false,
                disabled: true,
                id: 'StandardizationStep'
            },
            {
                title: 'Segment',
                directive: '',
                active: false,
                disabled: true,
                id: 'SegmentationStep'

            },
            {
                title: 'Match Schemas',
                directive: '',
                active: false,
                disabled: true,
                id: 'SchemaMatchingStep'

            },
            {
                title: 'Index',
                directive: '',
                active: false,
                disabled: true,
                id: 'IndexingStep'
            },
            {
                title: 'Compare',
                directive: '',
                active: false,
                disabled: true,
                id: 'ComparisonStep'
            },
            {
                title: 'Classify',
                directive: '',
                active: false,
                disabled: true,
                id: 'ClassificationStep'
            },
            {
                title: 'Fuse Data',
                directive: '',
                active: false,
                disabled: true,
                id: 'DataFusionStep'
            },
            {
                title: 'Export',
                directive: '',
                active: false,
                disabled: true,
                id: 'ExportStep'
            }
        ];

        function setCurrentStep() {
            var i = 0;
            for (tab in $scope.tabs) {
                if ($scope.tabs[tab].active) {
                    $scope.currentStep = i;
                    return;
                }
                i++;
            }
        }

        $scope.$watch('tabs', setCurrentStep, true);

    })
;