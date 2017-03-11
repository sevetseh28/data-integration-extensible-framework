/**
 * Created by Hernan on 23/2/2017.
 */
angular.module("materialAdmin")
    .directive('indexingPreview', function () {
        return {
            restrict: "E",
            templateUrl: "template/directives/data-preview/indexing-preview.html"
        }
    });