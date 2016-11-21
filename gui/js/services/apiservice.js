/**
 * Created by Hernan on 20/11/2016.
 */
angular.module('materialAdmin')
    .factory('APIService', function ($http) {

        function getData() {
            $http.get(apiurl)
                .success(function (data, status, config, headers) {
                    myData = data;
                })
                .error(function () { //handler errors here
                });
        }

        function getColumnsSource1() {
            return ['Full name', 'Phone', 'Address', 'ID']
        }

        function getColumnsSource2() {
            return ['Name', 'Surname', 'Phone', 'Country', 'Birthday']
        }

        function getOutputFields() {
            return [
                {
                    'matchedColumns': 'Full name <---> Name,Surname',
                    'outputFields': [{'name': 'Name'}, {'name': 'Last name'}]
                },
                {
                    'matchedColumns': 'Phone <---> Phone',
                    'outputFields': [{'name': 'Phone'}]
                }
            ]
        }

        function getModules(step) {
            // lamo al servicio y cargo en la variable modules de step los modulos disponibles
            if (step == 'standardisation') {
                return [
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
                return [{
                    'name': 'CSV Extractor',
                    'config': {
                        'path': {
                            'type': 'dropdown',
                            'label': 'Select one option',
                            'selectedoption': {},
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

            } else if (step == 'segmentation') {
                return [{
                    'name': 'No segmentation',
                    'config': {}
                }]

            } else if (step == 'schemamatching') {
                return [{
                    "name": "Manual Matching",
                    "config": {
                        "matches": {
                            "type": "rows",
                            "label": "Matches",
                            "rows": [],
                            "rowmodel": {
                                "type": "row",
                                "cols": [
                                    {
                                        "type": "multipleselect",
                                        "options": getColumnsSource1()
                                    },
                                    {
                                        "type": "multipleselect",
                                        "options": getColumnsSource2()
                                    }
                                ]
                            }
                        }
                    }
                }]

            } else if (step == 'comparison') {
                return [{
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
                    }]

            } else if (step == 'indexing') {
                return [{
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
                    }]
            }
        }

        return {
            getColumnsSource1: getColumnsSource1,
            getColumnsSource2: getColumnsSource2,
            getOutputFields: getOutputFields,
            getModules: getModules
        }
    });