/**
 * Created by Hernan on 23/2/2017.
 */
angular.module("materialAdmin")
    .directive('segmenteddataPreview', function () {
        return {
            scope: true,
            restrict: "E",
            templateUrl: "template/directives/data-preview/segmenteddata-preview.html"
        }
    });