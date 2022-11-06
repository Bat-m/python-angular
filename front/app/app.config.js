'use strict';

angular.
  module('interventionAPP').
  config(['$routeProvider',
    function config($routeProvider) {
      $routeProvider.
      when('/', {
        template: '<intervention-list></intervention-list>'
      });
    }
  ]);
