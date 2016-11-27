/**
 * Created by Hernan on 11/19/2016.
 */
angular.module("materialAdmin")
    .directive('rangesliderInput', function() {
        return {
            restrict: "E",
            scope: true,
            template: '<p class="f-500 c-black m-b-5">{{config.label}}</p>\
            <small class="c-gray">Current value: {{ config.from }} - {{ config.to }}</small>\
               <br/>\
                <br/>\
                <div slider class="input-slider-range" ng-from="config.from" ng-to="config.to" start={{config.start}} end={{config.end}} step={{config.step}}></div>',
            link: function (scope, element, attrs) {

                function appendReturnValue() {
                    scope.returnValue[scope.configId] = {
                        from: scope.config.from,
                        to: scope.config.to

                    }
                }

                scope.$watch('config', appendReturnValue, true);

            }
        }
    });