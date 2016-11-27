/**
 * Created by Hernan on 20/11/2016.
 */
angular.module('materialAdmin')
    .factory('APIService', function ($http, $q) {

        var baseUrl = 'http://localhost:8001/';

        function get(path, ignoreloadingbar) {
            var deferred = $q.defer();

            return $http.get(baseUrl + path + "/", {
                headers: {'Content-Type': 'application/json'}
            }).success(function (data) {
                deferred.resolve(data);
            });
        }

        function post(path, params, ignoreloadingbar) {
            var deferred = $q.defer();

            return $http.post(baseUrl + path + "/", params, {
                headers: {'Content-Type': 'application/json'}
            }).success(function (data) {
                deferred.resolve(data);
            });
        }


        function put(path, params, ignoreloadingbar) {
            var deferred = $q.defer();

            return $http.put(baseUrl + path + "/", params, {
                headers: {'Content-Type': 'application/json'}
            }).success(function (data) {
                deferred.resolve(data);
            });
        }

        function del(path, ignoreloadingbar) {
            var deferred = $q.defer();

            return $http.delete(baseUrl + path + "/", {
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
            var path = 'projects/' + idProject;
            return del(path);
        }

        function getColumnsSource1() {
            return ['Full name', 'Phone', 'Address', 'ID']
        }

        function getColumnsSource2() {
            return ['Name', 'Surname', 'Phone', 'Country', 'Birthday']
        }

        function getColumnsSources(idProject) {
            var path = 'columns/' + idProject;
            return get(path);
        }

        function getOutputFields() {
            return [
                {
                    "name": "Column0"
                }
            ]
        }

        function getModules(step) {
            // lamo al servicio y cargo en la variable modules de step los modulos disponibles
            if (step == 'extraction') {
                return [
                    {
                        "config": {
                            "config1": {
                                "type": "text",
                                "label": "coso"
                            }
                        },
                        "id": "dummy",
                        "name": "Dummy Module"
                    },
                    {
                        "config": {
                            "config1": {
                                "type": "text",
                                "label": "coso"
                            }
                        },
                        "id": "dummy",
                        "name": "Dummy Module2"
                    }
                ]

            } else if (step == 'standardisation') {
                return [
                    {
                        "config": {
                            "chars": {
                                "type": "text",
                                "label": "Characters to delete"
                            }
                        },
                        "id": "delete-chars",
                        "name": "Delete chars"
                    },
                    {
                        "config": {},
                        "id": "lowercase",
                        "name": "To lowercase"
                    }
                ]

            } else if (step == 'segmentation') {
                return [
                    {
                        "config": {},
                        "id": "nop",
                        "name": "Nop Segmentation"
                    }
                ]

            } else if (step == 'schemamatching') {
                return [
                    {
                        "config": {
                            "matches": {
                                "rows": [],
                                "type": "rows",
                                "rowmodel": {
                                    "type": "row",
                                    "cols": {
                                        "source2": {
                                            "type": "multipleselect",
                                            "options": [
                                                "Column0",
                                                "Column1",
                                                "Column2",
                                                "Column3",
                                                "Column4",
                                                "Column5",
                                                "Column6",
                                                "Column7",
                                                "Column8",
                                                "Column9"
                                            ]
                                        },
                                        "source1": {
                                            "type": "multipleselect",
                                            "options": [
                                                "Column0",
                                                "Column1",
                                                "Column2",
                                                "Column3",
                                                "Column4",
                                                "Column5",
                                                "Column6",
                                                "Column7",
                                                "Column8",
                                                "Column9"
                                            ]
                                        }
                                    }
                                },
                                "label": "Matches"
                            }
                        },
                        "id": "manual",
                        "name": "Manual matching"
                    }
                ]

            } else if (step == 'comparison') {
                return [
                    {
                        "name": "Equal",
                        "config": {},
                        "id": "equals",
                        "value": "equals",
                        "label": "Equal"
                    },
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

            } else if (step == 'indexing') {
                return [
                    {
                        "name": "Full index",
                        "config": {}
                    },
                    {
                        "config": {
                            "keys": {
                                "type": "multipleselect",
                                "options": [
                                    "__new__Column0"
                                ],
                                "label": "Keys"
                            },
                            "encoding": {
                                "type": "dropdown",
                                "options": [
                                    {
                                        "name": "Generic Module",
                                        "config": {
                                            "name": {
                                                "type": "hidden",
                                                "value": "nop"
                                            }
                                        },
                                        "id": "nop",
                                        "value": "nop",
                                        "label": "Generic Module"
                                    },
                                    {
                                        "name": "Generic Module",
                                        "config": {
                                            "first_n": {
                                                "end": 10,
                                                "color": "red",
                                                "value": 2,
                                                "label": "Value of N",
                                                "start": 1,
                                                "step": 1,
                                                "type": "slider"
                                            },
                                            "name": {
                                                "type": "hidden",
                                                "value": "first-n"
                                            }
                                        },
                                        "id": "first-n",
                                        "value": "first-n",
                                        "label": "Generic Module"
                                    },
                                ],
                                "selectedoption": {},
                                "label": "Select encoding"
                            }
                        },
                        "id": "blocking-standard",
                        "name": "Blocking Standard"
                        // "name": "Blocking standard",
                        // "config": {
                        //     "keys": {
                        //         "type": "rows",
                        //         "rows": [],
                        //         "rowmodel": {
                        //             "type": "row",
                        //             "cols": {
                        //                 key:{
                        //                     "type": "dropdown",
                        //                     'label': 'Select a column',
                        //                     'selectedoption': {},
                        //                     'options': [
                        //                         {
                        //                             "value": "__new__Column0",
                        //                             "label": "__new__Column0"
                        //                         }
                        //                     ]
                        //                 },
                        //                 encoding:{
                        //                     "type": "dropdown",
                        //                     'label': 'Select encoding',
                        //                     'selectedoption': {},
                        //                     'options': [
                        //                         {
                        //                             "id": "nop",
                        //                             "label": "Generic Module",
                        //                             config:{}
                        //                         },
                        //                         {
                        //                             'label': 'Soundex',
                        //                             'config': {}
                        //                         },
                        //                         {
                        //                             'label': 'Keep first N chars',
                        //                             'config': {
                        //                                 "n": {
                        //                                     "type": "slider",
                        //                                     "label": "Value of N",
                        //                                     "value": 2,
                        //                                     "start": 1,
                        //                                     "end": 10,
                        //                                     "step": 1,
                        //                                     "color": "red"
                        //                                 }
                        //                             }
                        //                         }
                        //                     ]
                        //                 }
                        //         }
                        //         }
                        //     }
                        // }
                    }]
            } else if (step == 'classification') {
                return [
                    {
                        "name": "Fellegi Sunter",
                        "config": {
                            "thresholds": {
                                "from": "0.5",
                                "to": "0.7",
                                "label": "Range for potential matches",
                                "start": "0",
                                "step": 0.01,
                                "end": "1",
                                "type": "rangeslider"
                            }
                        },
                        "id": "fellegi-sunter",
                        "value": "fellegi-sunter",
                        "label": "Fellegi Sunter"
                    }
                ]
            } else if (step == 'datafusion') {
                return [
                    {
                        "name": "Preferred source",
                        "config": {
                            "preferred-source": {
                                "type": "radio",
                                "options": [
                                    {
                                        "value": 1,
                                        "label": "Source 1"
                                    },
                                    {
                                        "value": 2,
                                        "label": "Source 2"
                                    }
                                ],
                                "label": "Select the preferred source"
                            }
                        },
                        "id": "preferred-source",
                        "value": "preferred-source",
                        "label": "Preferred source"
                    }
                ]
            } else if (step == 'export') {
                return [
                    {
                        "name": "MongoDB",
                        "config": {
                            "host": {
                                "type": "text",
                                "label": "Host"
                            },
                            "db": {
                                "type": "text",
                                "label": "Database"
                            },
                            "port": {
                                "type": "text",
                                "label": "Port"
                            },
                            "collection": {
                                "type": "text",
                                "label": "Collection"
                            }
                        },
                        "id": "mongodb",
                        "value": "mongodb",
                        "label": "MongoDB"
                    },
                    {
                        "name": "CSV",
                        "config": {}
                    }]
            }
        }

        function run(project_id, step, config) {
            var path = 'run';
            var params = {
                project_id: project_id,
                step: step,
                config: config
            };
            return post(path, params);
        }

        return {
            getColumnsSource1: getColumnsSource1,
            getColumnsSource2: getColumnsSource2,
            getColumnsSources: getColumnsSources,
            getOutputFields: getOutputFields,
            getModules: getModules,
            run: run,
            //Projects
            getProjects: getProjects,
            deleteProject: deleteProject,
            createProject: createProject,
        }
    });