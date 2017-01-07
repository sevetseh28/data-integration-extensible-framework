/**
 * Created by Hernan on 11/19/2016.
 */
/**
 * Created by Hernan on 11/19/2016.
 */
angular.module("materialAdmin")
    .directive('sliderInput', function() {
        return {
            restrict: "E",
            scope: true,
            template: '<p class="f-500 c-black m-b-5">{{config.label}}</p>\
                        <div class="fg-line">\
                            <small class="c-gray">Current value: {{config.value}}</small>\
                            <div slider class="input-slider m-b-25" style="margin-top: 15px" ng-model="config.value" \
                                start={{config.start}} end={{config.end}} step={{config.step}} \
                                data-is-color={{config.color}}>\
                            </div>\
                        </div>',
                        link: function (scope, element, attrs) {

                function appendReturnValue() {
                    scope.returnValue[scope.configId] = scope.config.value

                    if ('nestedCheck' in scope) {
                        scope.nestedCheck['check'] ++
                    }
                }

                scope.$watch('config', appendReturnValue, true);

            }
        }
    });