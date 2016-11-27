/**
 * Created by Hernan on 20/11/2016.
 */
angular.module("materialAdmin")
    .directive('dropdownInput', function () {
        return {
            restrict: "E",
            scope: true,
            templateUrl: "template/directives/dynamic-inputs/dropdown-input.html",
            link: function (scope, element, attrs) {

                scope.childReturnValues = [];
                scope.loadChildControls = function () {
                    for(var k in scope.config.selectedoption.config){
                        scope.childReturnValues[k] = {};
                    }
                };
                scope.loadChildControl = function (k) {
                    scope.childReturnValues[k] = {};
                };

                function appendReturnValue() {
                    var ret = {};

                    for (var id in scope.childReturnValues) {
                        ret[id] = scope.childReturnValues[id][id]
                    }

                    scope.returnValue[scope.configId] = ret
                }

                scope.$watch('config',appendReturnValue, true);

            }

        }

    });

// EXAMPLE OF A DROPDOWN
// 'inputName': {
//     'type': 'dropdown',
//         'label': 'Select one option',
//         'selectedoption': {  },
//     'options': [
//         {
//             'label': 'esto es un slider y un text input',
//             'config': {
//                 'input1': {
//                     "type": "slider",
//                     "label": "Chus a namber",
//                     "value": 0.5,
//                     "start": 0,
//                     "end": 1,
//                     "step": 0.1,
//                     "color": "amber"
//                 },
//                 'path': {
//                     'type': 'text',
//                     'name': 'Ponga el path'
//                 }
//             }
//         },
//         {
//             'label': 'esto es un checkbox',
//             'config': {
//                 'input2': {
//                     "type": "checkbox",
//                     "label": "Check some boxes",
//                     "options": [
//                         {"label": "Opcion 1", "value": false},
//                         {"label": "Opcion 2", "value": false}
//                     ]
//                 }
//             }
//         }
//     ]
// }