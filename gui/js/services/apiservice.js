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

        function getProject(idProject) {
            var path = 'projects/'+idProject;
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

        function getColumnsSources(idProject) {
            var path = 'columns/' + idProject;
            return get(path);
        }

        function getSegmentedSchema(idProject) {
            var path = 'segmented-schema/' + idProject;
            return get(path);
        }

        function getGlobalSchema(idProject) {
            var path = 'global-schema/' + idProject;
            return get(path);
        }

        function getComparisonInfo(idProject) {
            var path = 'comparison-data/' + idProject;
            return get(path);
        }

        function getClassificationInfo(idProject) {
            var path = 'matches-result/' + idProject;
            return get(path);
        }

        function getOutputFields(idProject) {
            var path = 'output-fields/'+idProject;
            return get(path);
        }

        function getModules(idProject, step) {
            var path = 'available-modules/'+step+'/'+idProject;
            return get(path);
        }

        function run(project_id, step, config, step_state) {
            var path = 'run';

            var params = {
                project_id: project_id,
                step: step,
                config: config,
                step_state: step_state
            };
            return post(path, params);
        }
        function downloadFile(filename,name){
            path = baseUrl+"download-file/"+filename+"/"+name+"/";
            window.open(path, '_blank', '');
        }

        function previewData(project_id, step) {
            var path = 'preview-data/' + step + '/'+project_id;
            return get(path);
        }

        return {
            getColumnsSources: getColumnsSources,
            getSegmentedSchema: getSegmentedSchema,
            getOutputFields: getOutputFields,
            getModules: getModules,
            run: run,

            //Projects
            getProjects: getProjects,
            getProject: getProject,
            deleteProject: deleteProject,
            createProject: createProject,

            //Download file
            downloadFile: downloadFile,

            previewData: previewData,
            getGlobalSchema: getGlobalSchema,
            getComparisonInfo: getComparisonInfo,
            getClassificationInfo: getClassificationInfo
        }
    });