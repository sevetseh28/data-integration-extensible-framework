materialAdmin

    //====================================
    // STEPS
    //====================================

    .controller('StepsCtrl', function ($scope, $window) {
        $scope.currentStep = 0;

        $scope.sources = ['source1', 'source2'];

        $scope.steps = [
            'extraction',
            'standardisation',
            'segmentation',
            'schemamatching',
            'indexing',
            'comparison'
        ];

        // Esta funcion es global y es llamada por cada directiva de step para cargar los modulos disponibles
        $scope.loadModules = function (step) {

            // lamo al servicio y cargo en la variable modules de step los modulos disponibles
            if (step == 'standardisation') {
                $scope[step]['modules'] = [
                    {
                        'name': 'Lowercase',
                        'config': {
                            'char': {
                                'type': 'text',
                                'name': 'nothing'
                            },
                            'char2': {
                                'type': 'text',
                                'name': 'nothing 2'
                            }
                        }
                    },
                    {
                        'name': 'Delete chars',
                        'config': {
                            'char': {
                                'type': 'text',
                                'name': 'Input char to delete'
                            }
                        }
                    }
                ]


            } else if (step == 'extraction') {
                $scope[step]['modules'] = {
                    'source1': [{
                        'name': 'CSV Extractor',
                        'config': {
                            'path': {
                                'type': 'dropdown',
                                'label': 'Select one option',
                                'selectedoption': {  },
                                'options': [
                                    {
                                        'label': 'esto es un slider',
                                        'config': {
                                            'input1': {
                                                "type": "slider",
                                                "label": "Chus a namber",
                                                "value": 0.5,
                                                "start": 0,
                                                "end": 1,
                                                "step": 0.1,
                                                "color": "amber"
                                            },
                                            'path': {
                                                'type': 'text',
                                                'name': 'Ponga el path'
                                            }
                                        }
                                    },
                                    {
                                        'label': 'esto es un checkbox',
                                        'config': {
                                            'input2': {
                                                "type": "checkbox",
                                                "label": "Check some boxes",
                                                "options": [
                                                    {"label": "Opcion 1", "value": false},
                                                    {"label": "Opcion 2", "value": false}
                                                ]
                                            }
                                        }
                                    }
                                ]
                            }
                        }
                    },
                    {
                        'name': 'PostgreSQL Extractor',
                        'config': {
                            'path': {
                                'type': 'text',
                                'name': 'Ponga el path'
                            }
                        }
                    },
                    {
                        'name': 'MongoDB Extractor',
                        'config': {
                            'path': {
                                'type': 'text',
                                'name': 'Ponga el path'
                            }
                        }
                    }]
                };
                $scope[step]['modules']['source2'] = angular.copy($scope[step]['modules']['source1'])

            } else if (step == 'segmentation') {

                $scope[step]['modules'] = [
                    {
                        'name': 'No segmentation',
                        'config': {}
                    }
                ]
            } else if (step == 'schemamatching') {
                $scope[step]['modules'] = [
                    {
                        "name": "Manual Matching",
                        "config": {
                            "matches": {
                                "type": "rows",
                                "label": "Matches",
                                "rows": [],
                                "rowmodel":
                                    {
                                        "type": "row",
                                        "cols": [
                                            {
                                                "type": "multipleselect",
                                                "options": [
                                                    "Column0",
                                                    "Column1"
                                                ]
                                            },
                                            {
                                                "type": "checkbox",
                                                "label": "Check some boxes",
                                                "options": [
                                                    {"label": "Opcion 1", "value": false},
                                                    {"label": "Opcion 2", "value": false}
                                                ]
                                            },
                                            {
                                                "type": "radio",
                                                "label": "Select something...",
                                                "selected": "",
                                                "inline": false,
                                                "options": [
                                                    {"label": "Opcion 1", "value": "opt1"},
                                                    {"label": "Opcion 2", "value": "opt2"}
                                                ]
                                            },
                                            {
                                                "type": "slider",
                                                "label": "Chus a namber",
                                                "value": 0.5,
                                                "start": 0,
                                                "end": 1,
                                                "step": 0.1,
                                                "color": "amber"
                                            }
                                        ]
                                    }

                                
                            }
                        }
                    }

                ]
            } else if (step == 'comparison') {
                $scope[step]['modules'] = [
                    {
                        "name": "Q-grams",
                        "config": {
                            "q": {
                                "type": "slider",
                                "label": "Size of Q-grams",
                                "value": 2,
                                "start": 1,
                                "end": 10,
                                "step": 1,
                                "color": "green"
                            }
                        }
                    },
                    {
                        "name": "Levenshtein edit distance",
                        "config": {}
                    }
                ]
            }  else if (step == 'indexing') {
                $scope[step]['modules'] = [
                    {
                        "name": "Full index",
                        "config": {}
                    },
                    {
                        "name": "Blocking standard",
                        "config": {
                            "blocking-key": {
                                "type": "rows",
                                "rows": [],
                                "rowmodel": {
                                    "type": "row",
                                    "cols": [
                                        {
                                            "type": "dropdown",
                                            'label': 'Select a column',
                                            'selectedoption': {},
                                            'options': [
                                                {
                                                    'label': 'Fullname <---> Nombre y apellido',
                                                    'config': {}
                                                },
                                                {
                                                    'label': 'Address <---> Address',
                                                    'config': {}
                                                }
                                            ]
                                        },
                                        {
                                            "type": "dropdown",
                                            'label': 'Select encoding',
                                            'selectedoption': {},
                                            'options': [
                                                {
                                                    'label': 'Soundex',
                                                    'config': {}
                                                },
                                                {
                                                    'label': 'Keep first N chars',
                                                    'config': {
                                                        "n": {
                                                            "type": "slider",
                                                            "label": "Value of N",
                                                            "value": 2,
                                                            "start": 1,
                                                            "end": 10,
                                                            "step": 1,
                                                            "color": "red"
                                                        }
                                                    }
                                                }
                                            ]
                                        }
                                    ]
                                }
                            }
                        }
                    }
                ]
            }

        };

        // INICIALIZACION DE OBJETOS DE steps
        $scope.extraction = {
            selectedModules: {
                'source1': { 'config': {} },
                'source2': { 'config': {} }
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
            selectedModule: {},
            modules: []
        };


        $scope.runCurrentStep = function () {
            //alert(JSON.stringify($scope.extraction.selectedModules['source1']['config']))
            $scope.tabs[$scope.currentStep]['active'] = false;
            $scope.currentStep = $scope.currentStep + 1;

            $scope.tabs[$scope.currentStep]['disabled'] = false;
            $scope.loadModules($scope.steps[$scope.currentStep]);
            $scope.tabs[$scope.currentStep]['active'] = true;

            //alert('Current step is now ' + $scope.tabs[$scope.currentStep]['title'] )
        };

        $scope.tabs = [
            {
                title: 'Extract',
                directive: 'extraction-step',
                active: true,
                disabled: false
            },
            {
                title: 'Standardise',
                directive: 'standardisation-step',
                active: false,
                disabled: true
            },
            {
                title: 'Segment',
                directive: '',
                active: false,
                disabled: true

            },
            {
                title: 'Match Schemas',
                directive: '',
                active: false,
                disabled: true

            },
            {
                title: 'Index',
                directive: '',
                active: false,
                disabled: true
            },
            {
                title: 'Compare',
                directive: '',
                active: false,
                disabled: true
            },
            {
                title: 'Classify',
                directive: '',
                active: false,
                disabled: true
            },
            {
                title: 'Fuse Data',
                directive: '',
                active: false,
                disabled: true
            },
            {
                title: 'Export',
                directive: '',
                active: false,
                disabled: true
            }
        ];

    });