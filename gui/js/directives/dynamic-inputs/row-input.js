angular.module("materialAdmin")
    .directive('rowInput', function () {
        return {
            restrict: "E",
            scope: true,
            templateUrl: "template/directives/dynamic-inputs/row-input.html",
            link: function (scope, element, attrs) {

                scope.childReturnValues = [];
                scope.nestedChecks = {};

                scope.loadChildControl = function (k) {
                    scope.childReturnValues[k] = {};
                };

                scope.loadNestedCheck = function (k) {
                    scope.nestedChecks[k] = {'check':0};
                };

                scope.initControls = function(k){
                    scope.loadChildControl(k);
                    scope.loadNestedCheck(k);
                };

                scope.getColClass = function() {
                    map = {1:'col-md-12', 2:'col-sm-6', 3:'col-sm-4', 4:'col-sm-3'};

                    return map[Object.keys(scope.config.cols).length]
                };

                function appendReturnValue() {
                    var ret = {};

                    for (var id in scope.childReturnValues) {
                        ret[id] = scope.childReturnValues[id][id]
                    }

                    scope.returnValue[scope.configId] = ret;

                    if(scope.nestedCheck){
                        scope.nestedCheck['check'] ++;
                    }
                }

                scope.$watch(function(){return scope.nestedChecks}, appendReturnValue, true);

            }
        }
    });