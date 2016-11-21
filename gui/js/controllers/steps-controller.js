materialAdmin

    //====================================
    // STEPS
    //====================================

    .controller('StepsCtrl', function (APIService, $scope) {
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

            // lamo al servicio y cargo en la variable modules de step los modulos disponibles
            if (step == 'standardisation') {
                $scope[step]['modules'] = APIService.getModules(step);
                $scope.standardisation['columns'] = {
                    'source1': APIService.getColumnsSource1(),
                    'source2': APIService.getColumnsSource2()
                }

            } else if (step == 'extraction') {
                $scope[step]['modules']['source1'] = APIService.getModules(step);
                $scope[step]['modules']['source2'] = angular.copy($scope[step]['modules']['source1']);

            } else if (step == 'segmentation') {
                $scope[step]['modules'] = APIService.getModules(step);

            } else if (step == 'schemamatching') {
                $scope[step]['modules'] = APIService.getModules(step);

            } else if (step == 'comparison') {
                $scope[step]['outputFields'] = APIService.getOutputFields();
                $scope[step]['modules'] = APIService.getModules(step);
                for (var i=0; i < $scope[step]['outputFields'].length; i++) {
                    for (var j=0; j < $scope[step]['outputFields'][i]['outputFields'].length; j++) {
                        $scope[step]['outputFields'][i]['outputFields'][j]['modules']  = angular.copy($scope[step]['modules']);
                        $scope[step]['outputFields'][i]['outputFields'][j]['selectedModule'] = { 'name': 'Test'};
                    }
                }

            }  else if (step == 'indexing') {
                $scope[step]['modules'] = APIService.getModules(step);
            } else if (step == 'classification') {
                $scope[step]['modules'] = APIService.getModules(step);
            } else if (step == 'datafusion') {
                $scope[step]['modules'] = APIService.getModules(step);
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
            //selectedModule: {},
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


        $scope.runCurrentStep = function () {
            $scope.tabs[$scope.currentStep]['active'] = false;
            $scope.currentStep = $scope.currentStep + 1;
            $scope.tabs[$scope.currentStep]['disabled'] = false;

            $scope.loadStep($scope.steps[$scope.currentStep]);

            $scope.tabs[$scope.currentStep]['active'] = true;
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