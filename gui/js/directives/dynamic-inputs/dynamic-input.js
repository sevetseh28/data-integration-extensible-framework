angular.module("materialAdmin")
.directive('dynamicInput', function($compile) {
    return {
        restrict: "E",
        template: "",
        scope: {
            config: '='
        },
        link: function(scope, element, attrs) {

           function compile_directive() {

                var directive = '<'+scope.config.type+'-input></'+scope.config.type+'-input>';
                /*
                $compile(directive)(scope, function(cloned, scope){
                    element.append(cloned);
                });*/
                element.html(directive);
                $compile(element.contents())(scope);
                //alert('Dynamic input compilado')
            }

            scope.$watch('config.type', compile_directive);

        },



    }
});