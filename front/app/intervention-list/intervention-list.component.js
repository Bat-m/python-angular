'use strict';

// Register `phoneList` component, along with its associated controller and template
angular.
  module('interventionList').
  component('interventionList', {
    templateUrl: 'intervention-list/intervention-list.template.html',
    controller: ['$http', '$scope',
      function InterventionsController($http, $scope) {
        var self = this;
        self.isOpen = false
        self.isOpenUpdate = false

        $scope.master = {};
        $scope.interventions = [];


        $scope.create = function (intervention) {
          $http.post('http://127.0.0.1:5000/create', intervention).then(function (response) {
            console.log('response: ', response)
            $scope.interventions = response.data;
            self.isOpen = false;
            $scope.reset();
          });
          //$scope.master = angular.copy(user);
        };

        self.openEdit = function openEdit(id) {
          $http.get(`http://127.0.0.1:5000/getone/${id}`).then(function (response) {
            console.log('response: ', response.data)
            self.intervention = response.data;
            self.isOpenUpdate = true;
          });
        };


        $scope.update = function (intervention, id) {
          $http.post(`http://127.0.0.1:5000/update/${id}`, intervention).then(function (response) {
            self.intervention = response.data;
            self.isOpenUpdate = false;

            $http.get('http://127.0.0.1:5000/getall').then(function (response) {
              $scope.interventions = response.data;
            });
          });
        };


        $scope.delete = function (id) {
          $http.post(`http://127.0.0.1:5000/delete/${id}`).then(function (response) {

            $http.get('http://127.0.0.1:5000/getall').then(function (response) {
              $scope.interventions = response.data;
            });
          });
        };

        $http.get('http://127.0.0.1:5000/getall').then(function (response) {
          $scope.interventions = response.data;
        });

        self.open = function open() {
          self.isOpen = !self.isOpen;
        };

        self.openUpdate = function openUpdate() {
          self.isOpenUpdate = !self.isOpenUpdate;
        };

        $scope.getAll = function () {
          console.log(self.orderBy)
          $http.get(`http://127.0.0.1:5000/getall?orderBy=${self.orderBy}`).then(function (response) {
            console.log(response.data)
            $scope.interventions = response.data;

          })
        };
      }
    ]
  });
