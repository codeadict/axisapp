angular.module('ReportingApp')
    .controller('DashboardController', [
        '$scope',
        function ($scope) {

            $scope.provinces = [
                'Azuay',
                'Pichincha',
                'Guayas',
            ];

            //$scope.weekly = weekChart;

            //$scope.perprovince = perProvinceChart;

            //$scope.perstatus = statusesChart;

            $scope.slides = {
                list: $scope.provinces,
                current: $scope.provinces[0],
                next: function () {
                    $scope.slides.move('right');
                },
                prev: function () {
                    $scope.slides.move('left');
                },
                move: function (type) {
                    var list = $scope.slides.list,
                        current = $scope.slides.current,
                        idxRight = list.indexOf(current) + 1,
                        idxLeft = (list.indexOf(current) || list.length) - 1,
                        idx = (type === 'right') ? idxRight : idxLeft;

                    $scope.slides.current = list[idx % list.length];

                    //$scope.perprovince.loadData($scope.banner.api, $scope.slides.current.name);
                }
            };
        }

    ]);