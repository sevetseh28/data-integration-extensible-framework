/**
 * Created by Hernan on 20/11/2016.
 */
angular.module('materialAdmin')
    .factory('APIService', function ($http, $q) {

        var baseUrl = 'http://localhost:8001/';

        function get(path, ignoreloadingbar) {
            var deferred = $q.defer();

            return $http.get(baseUrl+path+"/", {
                headers: {'Content-Type': 'application/json'}
            }).success(function (data) {
                deferred.resolve(data);
            });
        }

        function post(path, params, ignoreloadingbar) {
            var deferred = $q.defer();

            return $http.post(baseUrl+path+"/", params, {
                headers: {'Content-Type': 'application/json'}
            }).success(function (data) {
                deferred.resolve(data);
            });
        }


        function put(path, params, ignoreloadingbar) {
            var deferred = $q.defer();

            return $http.put(baseUrl+path+"/", params, {
                headers: {'Content-Type': 'application/json'}
            }).success(function (data) {
                deferred.resolve(data);
            });
        }

        function del(path, ignoreloadingbar) {
            var deferred = $q.defer();

            return $http.delete(baseUrl+path+"/", {
                headers: {'Content-Type': 'application/json'}
            }).success(function (data) {
                deferred.resolve(data);
            });
        }
        //
        // function getData() {
        //     $http.get(apiurl)
        //         .success(function (data, status, config, headers) {
        //             myData = data;
        //         })
        //         .error(function () { //handler errors here
        //         });
        // }

        function getProjects() {
            var path = 'projects';
            return get(path);
        }

        function createProject(project) {
            var path = 'projects';
            return post(path, project);
        }

        function deleteProject(idProject) {
            var path = 'projects/'+idProject;
            return del(path);
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
                                'label': 'nothing'
                            },
                            'char2': {
                                'type': 'text',
                                'label': 'nothing 2'
                            }
                        }
                    },
                    {
                        'name': 'Delete chars',
                        'config': {
                            'char': {
                                'type': 'text',
                                'label': 'Input char to delete'
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
                                            'label': 'Ponga el path'
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
                                'label': 'Ponga el path'
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
            } else if (step == 'classification') {
                return [{
                    "name": "Fellegi & Stunter",
                    "config": {
                        "potentialmatches": {
                            "type": "rangeslider",
                            "label": "Range for potential matches",
                            "start": "0",
                            "end": "1",
                            "from": "0.5",
                            "to": "0.7",
                            "step": 0.01
                        }
                    }
                }]
            } else if (step == 'datafusion') {
                return [{
                    "name": "Source preference",
                    "config": {
                        "potentialmatches": {
                            "type": "radio",
                            "label": "Select the source to prefer",
                            "options": [
                                {"value": 1, "label": "Source 1"},
                                {"value": 2, "label": "Source 2"}
                            ]
                        }
                    }
                }]
            } else if (step == 'export') {
                return [{
                    "name": "MongoDB",
                    "config": {
                        "ip": {
                            "type": "text",
                            "label": "Database IP address"
                        },
                        "user": {
                            "type": "text",
                            "label": "Username"
                        },
                        "pass": {
                            "type": "text",
                            "label": "Password"
                        },
                        "db": {
                            "type": "text",
                            "label": "Database name"
                        },
                        "collection": {
                            "type": "text",
                            "label": "Collection name"
                        }
                    }
                },
                {
                    "name": "CSV",
                    "config": {}
                }]
            }
        }

        return {
            getColumnsSource1: getColumnsSource1,
            getColumnsSource2: getColumnsSource2,
            getOutputFields: getOutputFields,
            getModules: getModules,
            //Projects
            getProjects:getProjects,
            deleteProject:deleteProject,
            createProject:createProject,
        }
    });