materialAdmin

//====================================
// STEPS
//====================================

    .controller('ProjectsCtrl', function (APIService, $scope, $location) {
        $scope.allProjects = [];
        $scope.newProject = {stepconfig_set: []};

        $scope.reloadProjects = function () {
            APIService.getProjects().then(function (response) {
                $scope.allProjects = response.data;
            });
        };
        $scope.reloadProjects();

        $scope.deleteProject = function (idProject) {
            APIService.deleteProject(idProject).then(function () {
                $scope.reloadProjects()
            })
        };
        $scope.getScriptProject = function (idProject) {
            APIService.getScriptProject(idProject);
        };

        $scope.createProject = function () {
            APIService.createProject($scope.newProject).then(function () {
                $scope.newProject.name = "";
                $scope.reloadProjects();
            })
        };

        $scope.go = function (path) {
            $location.path(path);
        };

    });