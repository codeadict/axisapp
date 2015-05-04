/**
 * Created by codeadict on 5/2/15.
 */

var employeeTrackingApp = angular.module('employeeTrackingApp', ['ui.bootstrap', 'ngMaterial', 'uiGmapgoogle-maps'])
  .config(function ($interpolateProvider) {
    $interpolateProvider.startSymbol('[[').endSymbol(']]');
  })
  .config(function ($httpProvider) {
    $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
  })

  .config(function ($mdThemingProvider) {
    $mdThemingProvider.theme('default')
    .primaryPalette('orange')
    .accentPalette('teal')
    .dark();
  })
  .config(function (uiGmapGoogleMapApiProvider) {
    uiGmapGoogleMapApiProvider.configure({
      //    key: 'your api key',
      v: '3.17',
      libraries: 'geometry,visualization'
    });
  });

employeeTrackingApp.controller('TrackingController', function ($scope, uiGmapGoogleMapApi, $http, $interval) {

  $scope.options = {scrollwheel: false};
  uiGmapGoogleMapApi.then(function (maps) {
    $scope.map = { center: { latitude: -0.180653, longitude: -78.467834 }, zoom: 7 };
  });

  $scope.today = moment();
  if (localStorage.getItem('date')) {
    $scope.date = moment(localStorage.getItem('date')).toDate();
  } else {
    $scope.date = $scope.today.toDate();
  }

  var now = new Date(); //Step 1

  now.setMinutes(0);    //Step 2

  $scope.times = {
    selected: now.getTime(),   //Step 3
    step: 900000,         //Step 4
    from: now.setHours(now.getHours() - 6),  //Step 5
    to: now.setHours(now.getHours() + 12)
  }

  $scope.date_str = function () {
    return moment($scope.date).format('DD.MM.YYYY');
  };

});