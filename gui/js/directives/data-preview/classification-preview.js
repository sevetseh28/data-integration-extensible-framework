/**
 * Created by Hernan on 23/2/2017.
 */
angular.module("materialAdmin")
    .directive('classificationPreview', function () {
        return {
            restrict: "E",
            templateUrl: "template/directives/data-preview/classification-preview.html",
            link: function (scope, element, attrs) {
            },
            controller: function ($scope) {

            }
        }
    });