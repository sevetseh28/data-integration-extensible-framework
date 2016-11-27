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
            <small class="c-gray">Current value: {{config.value}}</small>\
               <br/>\
                <br/>\
            <div slider class="input-slider m-b-25" ng-model="config.value" start={{config.start}} end={{config.end}} step={{config.step}} data-is-color={{config.color}}></div>',
            link: function (scope, element, attrs) {

                function appendReturnValue() {
                    scope.returnValue[scope.configId] = scope.config.value
                }

                scope.$watch('config', appendReturnValue, true);

            }
        }
    });