materialAdmin

//====================================
// STEPS
//====================================

    .controller('StepsCtrl', function (APIService, $scope, $stateParams) {
        $scope.currentStep = 0;

        $scope.sources = ['source1', 'source2'];

        $scope.steps = [
            'extraction',
            'datacleansing',
            'standardisationtagging',
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

            } else if (step == 'datacleansing') {
                APIService.getModules($stateParams.id, step).then(function (data) {
                    $scope[step]['modules'] = data.data;
                });

                APIService.getColumnsSources($stateParams.id).then(function (response) {
                    $scope[step]['columns'] = {
                        'source1': response.data.source1,
                        'source2': response.data.source2
                    }
                });

                APIService.previewData($stateParams.id, 'ExtractionStep').then(function (response) {
                    $scope[step]['previewdata'] = {
                        'source1': response.data.source1,
                        'source2': response.data.source2
                    }
                });

                APIService.getColumnsSources($stateParams.id).then(function (response) {
                    $scope[step]['previewdataschema'] = {
                        'source1': response.data.source1,
                        'source2': response.data.source2
                    }
                });

            } else if (step == 'standardisationtagging') {
                $scope.standardisationtagging['moduleSelections'] = {};
                $scope.standardisationtagging['moduleSelections']['source1'] = [];
                $scope.standardisationtagging['moduleSelections']['source2'] = [];

                APIService.getModules($stateParams.id, step).then(function (data) {
                    $scope[step]['modules'] = data.data;
                });

                APIService.getColumnsSources($stateParams.id).then(function (response) {
                    $scope.standardisationtagging['columns'] = {
                        'source1': response.data.source1,
                        'source2': response.data.source2
                    };

                    for (var i = 0; i < $scope.standardisationtagging['columns']['source1'].length; i++) {

                        var column = {
                            'column': $scope.standardisationtagging['columns']['source1'][i],
                            'modules': angular.copy($scope.standardisationtagging['modules']),
                            'selectedModule': {}
                        };
                        $scope.standardisationtagging['moduleSelections']['source1']
                            .push(column);

                    }

                    for (var i = 0; i < $scope.standardisationtagging['columns']['source2'].length; i++) {
                        var column = {
                            'column': $scope.standardisationtagging['columns']['source2'][i],
                            'modules': angular.copy($scope.standardisationtagging['modules']),
                            'selectedModule': {}
                        };
                        $scope.standardisationtagging['moduleSelections']['source2']
                            .push(column);
                    }

                });

                APIService.previewData($stateParams.id, 'DataCleansingStep').then(function (response) {
                    $scope[step]['previewdata'] = {
                        'source1': response.data.source1,
                        'source2': response.data.source2
                    }
                });

                APIService.getColumnsSources($stateParams.id).then(function (response) {
                    $scope[step]['previewdataschema'] = {
                        'source1': response.data.source1,
                        'source2': response.data.source2
                    }
                });


            } else if (step == 'segmentation') {
                $scope.segmentation['moduleSelections'] = {};
                $scope.segmentation['moduleSelections']['source1'] = [];
                $scope.segmentation['moduleSelections']['source2'] = [];

                APIService.previewData($stateParams.id, 'StandardisationAndTaggingStep').then(function (response) {
                    $scope[step]['previewdata'] = {
                        'source1': response.data.source1,
                        'source2': response.data.source2
                    }
                });

                APIService.getColumnsSources($stateParams.id).then(function (response) {
                    $scope[step]['previewdataschema'] = {
                        'source1': response.data.source1,
                        'source2': response.data.source2
                    }
                });

                APIService.getModules($stateParams.id, step).then(function (data) {
                    $scope[step]['modules'] = data.data;
                });

                APIService.getColumnsSources($stateParams.id).then(function (response) {
                    $scope.segmentation['columns'] = {
                        'source1': response.data.source1,
                        'source2': response.data.source2
                    };

                    for (var i = 0; i < $scope.segmentation['columns']['source1'].length; i++) {

                        var column = {
                            'column': $scope.segmentation['columns']['source1'][i],
                            'modules': angular.copy($scope.segmentation['modules']),
                            'selectedModule': {}
                        };
                        $scope.segmentation['moduleSelections']['source1']
                            .push(column);

                    }

                    for (var i = 0; i < $scope.segmentation['columns']['source2'].length; i++) {
                        var column = {
                            'column': $scope.segmentation['columns']['source2'][i],
                            'modules': angular.copy($scope.segmentation['modules']),
                            'selectedModule': {}
                        };
                        $scope.segmentation['moduleSelections']['source2']
                            .push(column);
                    }

                });

            } else if (step == 'schemamatching') {
                $scope[step].selectedModule = {};
                APIService.getModules($stateParams.id, step).then(function (data) {
                    $scope[step]['modules'] = data.data;
                });

                APIService.previewData($stateParams.id, 'SegmentationStep').then(function (response) {
                    $scope[step]['previewdata'] = {
                        'source1': response.data.source1,
                        'source2': response.data.source2
                    }
                });

                APIService.getSegmentedSchema($stateParams.id).then(function (response) {
                    $scope[step]['previewdataschema'] = {
                        'source1': response.data.source1,
                        'source2': response.data.source2
                    }
                });

            } else if (step == 'comparison') {
                APIService.getOutputFields($stateParams.id).then(function (data) {
                    $scope[step]['outputFields'] = data.data.values;
                    $scope[step]['col_or_outputfield'] = data.data.col_or_outputfield;

                    APIService.getModules($stateParams.id, step).then(function (data) {
                        $scope[step]['modules'] = data.data;
                        for (var i = 0; i < $scope[step]['outputFields'].length; i++) {
                            $scope[step]['outputFields'][i]['modules'] = angular.copy($scope[step]['modules']);
                            $scope[step]['outputFields'][i]['selectedModule'] = {};
                        }
                    });

                    APIService.getIndexingInfo($stateParams.id).then(function (response) {
                        $scope[step]['idxinfo'] = response.data;
                    });


                });

                APIService.getComparisonInfo($stateParams.id).then(function (response) {
                    $scope[step]['previewdata'] = {
                        'source1': response.data.source1,
                        'source2': response.data.source2
                    }
                });

                APIService.getSegmentedSchema($stateParams.id).then(function (response) {
                    $scope[step]['previewdataschema'] = {
                        'source1': response.data.source1,
                        'source2': response.data.source2
                    }
                });

            } else if (step == 'indexing') {
                $scope[step].selectedModule = {};
                APIService.getModules($stateParams.id, step).then(function (response) {
                    $scope[step]['modules'] = response.data;
                });

                APIService.getGlobalSchema($stateParams.id).then(function (response) {
                    $scope[step]['previewdataschema'] = response.data
                });

            } else if (step == 'classification') {
                $scope[step].selectedModule = {};
                APIService.getModules($stateParams.id, step).then(function (data) {
                    $scope[step]['modules'] = data.data;
                });

                APIService.getComparisonInfo($stateParams.id).then(function (response) {
                    $scope[step]['comparisoninfo'] = response.data
                });

                APIService.getGlobalSchema($stateParams.id).then(function (response) {
                    $scope[step]['previewdataschema'] = response.data
                });


            } else if (step == 'datafusion') {
                $scope[step].selectedModule = {};
                APIService.getModules($stateParams.id, step).then(function (data) {
                    $scope[step]['modules'] = data.data;
                });

                APIService.getClassificationInfo($stateParams.id).then(function (response) {
                    $scope[step]['classificationinfo'] = response.data
                });

                APIService.getGlobalSchema($stateParams.id).then(function (response) {
                    $scope[step]['previewdataschema'] = response.data
                });

            } else if (step == 'export') {
                $scope[step].selectedModule = {};
                APIService.getModules($stateParams.id, step).then(function (data) {
                    $scope[step]['modules'] = data.data;
                });

                APIService.getFusedData($stateParams.id).then(function (response) {
                    $scope[step]['previewdata'] = response.data
                });

            }
        };

        // INICIALIZACION DE OBJETOS DE steps
        $scope.extraction = {
            selectedModules: {
                'source1': {'config': {}},
                'source2': {'config': {}}
            },
            modules: {}
        };

        $scope.datacleansing = {
            selectedModules: {
                'source1': [],
                'source2': []
            },
            modules: [],
            columns: {}
        };

        $scope.standardisationtagging = {
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

        function loadProjectState() {
            APIService.getProject($stateParams.id).then(function (response) {
                var steps = response.data.steps;

                $scope.projectName = response.data.name;

                if (steps.length == 0) {
                    $scope.loadStep('extraction');
                    return;
                }

                if(response.data.steps.length>=4){
                    $scope['segmentationskipped'] = response.data.steps[3].config.toggleskip.config.checked;
                    $scope.segmentation.toggleskip.config.checked = response.data.steps[3].config.toggleskip.config.checked;
                }

                for (var i = 0; i < steps.length; i++) {

                    if(i==9)
                        break;
                    //se carga el estado del step
                    var step = steps[i];
                    // var state = steps[i].config;
                    //
                    // // si el step actual es extraccion o standardization
                    // if(['ExtractionStep'].indexOf(step.step) != -1){
                    //     //copio el selectedModule a la lista de modulos para que quede 2 way binded
                    //     for(s=1;s<=2;s++){
                    //         for(var j=0;j<state.modules['source'+s].length;j++){
                    //             if(state.selectedModules['source'+s].id == state.modules['source'+s][j].id){
                    //                 state.modules['source'+s][j] = state.selectedModules['source'+s]
                    //             }
                    //         }
                    //     }
                    // }

                    // $scope[$scope.steps[i]] = state;

                    //se habilita la tab actual y la proxima
                    $scope.tabs[i].disabled = false;
                    $scope.tabs[i].reload_required = true;
                    $scope.tabs[i + 1].disabled = false;
                    $scope.tabs[i + 1].reload_required = true;

                    //se saca el active a este step
                    $scope.tabs[i].active = false;

                    //se pone como activo el step proximo
                    $scope.tabs[i + 1].active = true;

                    // Si se llego al ultimo step ejecutado, se deja de cargar para evitar cargar steps que se ejecutaron
                    // pero luego se ejecuto un step anterior a ese
                    if (response.data.current_step == $scope.tabs[i].id)
                        break;
                }

            })
        }

        loadProjectState();


        $scope.runCurrentStep = function () {
            stepId = $scope.tabs[$scope.currentStep].id;
            stepName = $scope.steps[$scope.currentStep];

            APIService.run($stateParams.id, stepId, $scope[stepName].returnValue, $scope[stepName]).then(function (data) {
                    if($scope.currentStep < 9){
                        $scope.tabs[$scope.currentStep]['active'] = false;
                        $scope.currentStep = $scope.currentStep + 1;
                        disableFollowingSteps();
                        if ($scope.tabs[$scope.currentStep]) {
                            if ($scope.steps[$scope.currentStep - 1] == 'segmentation') {
                                $scope['segmentationskipped'] = $scope.segmentation.toggleskip.config.checked;
                            }

                            $scope.tabs[$scope.currentStep]['disabled'] = false;
                            $scope.loadStep($scope.steps[$scope.currentStep]);

                        }

                        $scope.tabs[$scope.currentStep]['active'] = true;
                    }else{
                        swal({
                            title: "Data exported succesfully!",
                            type: "success",
                            text: '',
                            confirmButtonText: "OK"
                        });
                    }
                    if (data.data && data.data.downloadfile) {
                            APIService.downloadFile(data.data.downloadfile.filename, data.data.downloadfile.name);
                    }
                }, function (response) {
                    swal({
                            title: "An error has occured!",
                            type: "error",
                            text: 'Please check modules are selected and fully configured',
                            showCancelButton: true,
                            confirmButtonText: "OK",
                            cancelButtonText: "See details",
                            closeOnConfirm: true,
                            closeOnCancel: false
                        },
                        function (isConfirm) {
                            if (!isConfirm) {
                                swal({
                                        title: "Error details",
                                        text: response.data.details,
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
                directive: '',
                active: true,
                disabled: false,
                id: 'ExtractionStep'
            },
            {
                title: 'Cleanse',
                directive: '',
                active: false,
                disabled: true,
                id: 'DataCleansingStep'
            },
            {
                title: 'Standardise & Tag',
                directive: '',
                active: false,
                disabled: true,
                id: 'StandardisationAndTaggingStep'
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

        function disableFollowingSteps() {
            for (var i = $scope.currentStep + 1; i < $scope.tabs.length; i++)
                $scope.tabs[i].disabled = true;
        }

        function setCurrentStep() {
            var i = 0;
            for (tab in $scope.tabs) {
                if ($scope.tabs[tab].active) {
                    $scope.currentStep = i;
                    if ($scope.tabs[tab].reload_required) {
                        $scope.loadStep($scope.steps[tab]);
                        $scope.tabs[tab].reload_required = false
                    }
                    return;
                }
                i++;
            }
        }

        $scope.$watch('tabs', setCurrentStep, true);

    })
;