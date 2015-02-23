"use strict";

var $ = require('jquery'),
    U = require('treemap/utility'),
    Bacon = require('baconjs'),
    BU = require('treemap/baconUtils'),
    History = require('history');

var csrf = require('treemap/csrf');
$.ajaxSetup(csrf.jqueryAjaxSetupOptions);

exports.init = function(options) {
    var updatePageFromUrl = new Bacon.Bus(),
        url = options.url,
        nextPhotoUrl = options.nextPhotoUrl,
        $container = $(options.container),
        initialPageStream = updatePageFromUrl
            .map(U.parseQueryString)
            .map('.n')
            .filter(BU.id);

    window.addEventListener('popstate', function(event) {
        updatePageFromUrl.push();
    }, false);

    function showErrorMessage(msg) {
        $container.find('.errors').html(msg);
    }

    function getReviewMarkupForNextPhoto() {
        var n = U.parseQueryString.n || 1;
        return BU.jsonRequest('GET', nextPhotoUrl)({n: n});
    }

    function nextPageExists() {
        return !!$container.find('.pagination li:last-child [data-page]').attr('data-page');
    }

    $container.on('click', '.action', function(e) {
        e.preventDefault();
        var $photo = $(this).closest('[data-photo]');

        var stream = BU.jsonRequest('POST', $(this).attr('href'))();

        stream.onValue(function() {
            $photo.remove();
        });
        stream.onError(showErrorMessage);

        if (nextPageExists()) {
            stream
                .flatMap(getReviewMarkupForNextPhoto)
                .map($)
                .onValue($container.find('[data-photo-container]'), 'append');
        }
    });

    function createPageUpdateStream(initialPageStream) {
        var pageStream = $container.find('.pagination li')
                .asEventStream('click')
                .map('.target')
                .map($)
                .map('.data', 'page')
                .filter(BU.isDefinedNonEmpty);

        pageStream
            .map(function(n) { return '?n=' + n + window.location.hash; })
            .onValue(function (url) {
                History.pushState(null, document.title, url);
            });

        var pageUpdateStream = pageStream
                .merge(initialPageStream)
                .map(function(n) { return {'n': n}; })
                .flatMap(BU.jsonRequest('GET', url));

        pageUpdateStream
            .onValue($container, 'html');

        pageUpdateStream
            .onValue(createPageUpdateStream, initialPageStream);

        return pageUpdateStream;
    }

    createPageUpdateStream(initialPageStream);
};
