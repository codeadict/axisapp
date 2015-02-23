"use strict";

var $ = require('jquery'),
    _ = require('lodash'),
    L = require('leaflet'),
    toastr = require('toastr'),
    otmTypeahead = require('treemap/otmTypeahead'),
    plotMover = require('treemap/plotMover'),
    diameterCalculator = require('treemap/diameterCalculator'),
    reverseGeocodeStreamAndUpdateAddressesOnForm =
        require('treemap/reverseGeocodeStreamAndUpdateAddressesOnForm');


var formSelector = '#details-form',
    mapManager,
    inlineEditForm,
    typeaheads,
    plotMarker,
    calculator,
    currentPlotMover;

function init(options) {
    mapManager = options.mapManager;
    inlineEditForm = options.inlineEditForm;
    typeaheads = options.typeaheads;
    plotMarker = options.plotMarker;

    var markerMoveStream = plotMarker.moveStream.filter(options.inMyMode);
    reverseGeocodeStreamAndUpdateAddressesOnForm(
        options.config, markerMoveStream, formSelector);
}

function onClick(e) { 
    toastr.options = {
        "positionClass": "toast-bottom-left",
        "timeOut": "3000"
    };
    toastr.info('Click "Save" or "Cancel" to end your Quick Edit session.');
}

function activate() {
    otmTypeahead.bulkCreate(typeaheads);

    currentPlotMover = plotMover.init({
        mapManager: mapManager,
        plotMarker: plotMarker,
        inlineEditForm: inlineEditForm,
        editLocationButton: '#edit-plot-location',
        cancelEditLocationButton: '#cancel-edit-plot-location',
        location: plotMarker.getLocation()
    });

    calculator = diameterCalculator({
        formSelector: formSelector,
        cancelStream: inlineEditForm.cancelStream,
        saveOkStream: inlineEditForm.saveOkStream
    });

    mapManager.map.on('click', onClick);

}

function deactivate() {
    calculator.destroy();
    inlineEditForm.cancel();

    mapManager.map.off('click', onClick);
}

function onSaveBefore(data) {
    if (currentPlotMover) {
        currentPlotMover.onSaveBefore(data);
    }
}

module.exports = {
    name: 'editTreeDetails',
    init: init,
    activate: activate,
    deactivate: deactivate,
    onSaveBefore: onSaveBefore,
    lockOnActivate: true
};
