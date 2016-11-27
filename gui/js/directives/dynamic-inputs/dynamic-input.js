angular.module("materialAdmin")
    .directive('dynamicInput', function ($compile) {
        return {
            restrict: "E",
            template: "",
            scope: {
                config: '=',
                returnValue: '=',
                configId: '@',
                nestedCheck: '=?'
            },
            link: function (scope, element, attrs) {

                scope.returnValue = scope.returnValue || {};

                scope.debug = function(){
                    scope.config.a=1;
                    2+2
                };

                function compile_directive() {

                    var directive = '<' + scope.config.type + '-input></' + scope.config.type + '-input><button ng-click="debug()">lala</button>';
                    /*
                     $compile(directive)(scope, function(cloned, scope){
                     element.append(cloned);
                     });*/
                    element.html(directive);
                    $compile(element.contents())(scope);
                    //alert('Dynamic input compilado')
                }

                scope.$watch('config.type', compile_directive);


            }


        }
    });