angular.module("materialAdmin")
    .directive('radioinlineInput', function() {
        return {
            restrict: "E",
            scope: true,
            template: "<p class='c-black f-500 m-b-20'>{{config.label}}</p>\
                        <form>\
                            <div class='radio radio-inline m-b-15' ng-repeat='o in config.options'>\
                                <label>\
                                    <input type='radio' value='{{o.value}}' ng-model='config.selected'>\
                                    <i class='input-helper'></i>\
                                    {{o.label}}\
                                </label>\
                            </div>\
                        </form>",
            link: function (scope, element, attrs) {

                function appendReturnValue() {
                    scope.returnValue[scope.configId] = scope.config.selected;

                    if ('nestedCheck' in scope) {
                        scope.nestedCheck['check'] ++
                    }
                }

                scope.$watch('config', appendReturnValue, true);

            }
        }
    });