angular.module('ReportingApp',  [])
    .factory('chartSize', function () {
        return function (element) {
            return {
                width: parseInt(element.css('width').replace('px', ''), 10),
                height: 200
            };
        };
    })
    .factory('compressNumber', [function () {
        //compress a big number more than 100 in something more readable
        var mil = 1000,
            millon = mil * 1000,
            billon = millon * 1000,
            trillon = billon * 1000;

        return function (number) {
            var value = number, label = '';

            if (number > trillon) {
                label = 'Trillones';
                value = number / trillon;
            }
            else if (number > billon) {
                label = 'Billones';
                value = number / billon;
            }
            else if (number > millon) {
                label = 'Millones';
                value = number / millon;
            }
            else if (number > mil) {
                label = 'Mil';
                value = number / mil;
            }

            return {value: value, label: label};
        };
    }])
    .run(function () {
        //never cycle the carousel
        delete($.fn.carousel.Constructor.DEFAULTS.interval);
    });
