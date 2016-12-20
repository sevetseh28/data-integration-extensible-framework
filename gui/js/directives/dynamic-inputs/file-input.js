angular.module("materialAdmin")
    .directive('fileInput', function () {
        return {
            restrict: "E",
            scope: true,
            templateUrl: "template/directives/dynamic-inputs/file-input.html",
            controller: function ($scope, Upload, $timeout) {
                $scope.uploadCSV = function (file, errFiles) {
                    $scope.f = file;
                    $scope.errFile = errFiles && errFiles[0];
                    if (file) {
                        file.upload = Upload.upload({
                            url: 'http://localhost:8001/upload-file',
                            data: {file: file}
                        });

                        file.upload.then(function (response) {
                            $timeout(function () {
                                file.result = response.data;
                                $scope.config.location = response.data.location;
                            });
                        }, function (response) {
                            if (response.status > 0)
                                $scope.errorMsg = response.status + ': ' + response.data;
                        }, function (evt) {
                            file.progress = Math.min(100, parseInt(100.0 *
                                evt.loaded / evt.total));
                        });
                    }
                };

                function appendReturnValue() {
                    $scope.returnValue[$scope.configId] = $scope.config.location;

                    if ('nestedCheck' in $scope) {
                        $scope.nestedCheck['check'] ++
                    }
                }

                $scope.$watch('config', appendReturnValue, true);
            }
        }
    });