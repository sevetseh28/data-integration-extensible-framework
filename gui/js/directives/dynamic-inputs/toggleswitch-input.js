/**
 * Created by Hernan on 11/19/2016.
 */
angular.module("materialAdmin")
    .directive('toggleswitchInput', function() {
        return {
            restrict: "E",
            scope: true,
            template: '<div class="toggle-switch" data-ts-color="{{config.color}}">\
                            <label class="ts-label">{{config.label}}</label>\
                            <input type="checkbox" hidden="hidden" ng-model="config.checked">\
                            <label class="ts-helper" ng-click="toggle()"></label>\
                        </div>',
            controller: function ($scope) {
                $scope.toggle = function() {
                    $scope.config.checked = !($scope.config.checked)
                }
            }
        }
    });