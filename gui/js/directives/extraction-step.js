angular.module("materialAdmin")
.directive('extractionStep', function() {
    return {
        restrict: "E",
        templateUrl: "template/directives/extraction-step.html",
        controller: function ($scope) {

            $scope.extraction['title'] = 'Extraction';
            $scope.loadModules('extraction');

            $scope.displayModuleGUISource1 = function (moduleName) {
                $scope.extraction['isSelectedSource1'] = true;
                

            };


            $scope.displayModuleGUISource2 = function (moduleName) {
                $scope.extraction['isSelectedSource2'] = true;
                alert('Module has been changed to ' + moduleName)
                // aca hay que llamar al servicio que genera los campos y cargarlo en la primer columna
                

            };
        },
        link: function(scope) {
            scope.loadModules('extraction');
        }
    }
});