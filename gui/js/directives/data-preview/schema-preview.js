/**
 * Created by Hernan on 23/2/2017.
 */
angular.module("materialAdmin")
    .directive('schemaPreview', function () {
        return {
            restrict: "E",
            templateUrl: "template/directives/data-preview/schema-preview.html"
        }
    });