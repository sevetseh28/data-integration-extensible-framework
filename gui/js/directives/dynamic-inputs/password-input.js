angular.module("materialAdmin")
    .directive('passwordInput', function () {
        return {
            restrict: "E",
            scope: true,
            template: '<div class="form-group fg-float">\
                                <div class="fg-line">\
                                    <input type="password" ng-model="config.value" class="form-control fg-input" >\
                                </div>\
                                <label class="fg-label">{{config.label}}</label>\
                            </div>',
            link: function (scope, element, attrs) {

                function appendReturnValue() {
                    scope.returnValue[scope.configId] = scope.config.value;

                    if ('nestedCheck' in scope) {
                        scope.nestedCheck['check']++
                    }
                }

                scope.$watch('config', appendReturnValue, true);

            }

        }
    });