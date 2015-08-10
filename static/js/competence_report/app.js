var competenceReportApp = angular.module('competenceReportApp', ['ui.bootstrap', 'ngMaterial', 'uiGmapgoogle-maps'])
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

competenceReportApp.controller('CompetenceController', function ($scope, uiGmapGoogleMapApi, $http, $interval) {
    $scope.tabs = {
        "map": false,
        "list": true
    };

    $scope.selectedMarker = 0;

    $scope.listView = function () {
        $scope.tabs = {
            "map": false,
            "list": true
        };
    };

    $scope.mapView = function () {
        $scope.tabs = {
            "map": true,
            "list": false
        };
    };
    $scope.options = {scrollwheel: false};
    uiGmapGoogleMapApi.then(function (maps) {
        $scope.map = {center: {latitude: -0.180653, longitude: -78.467834}, zoom: 7};
    });
});