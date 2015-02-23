function set_contractor_list(data){
  $('#tokenfield_contractor').tokenfield({
    autocomplete: {
      source: data,
      delay: 100
    },
    showAutocompleteOnFocus: true
  });

  $('#tokenfield_contractor').on('tokenfield:createtoken', function (e) {
    var value = e.attrs.value;
    var list = $('#tokenfield_contractor').tokenfield('getTokensList').split(', ');
    inData = $.inArray(value, data);
    inList = $.inArray(value, list);
    if (inData<0 || inList>=0) {
      return false;
    }
  });
}

function set_recipient_list(data){
  $('#tokenfield_recipient').tokenfield({
    autocomplete: {
      source: data,
      delay: 100
    },
    showAutocompleteOnFocus: true
  });

  $('#tokenfield_recipient').on('tokenfield:createtoken', function (e) {
    var value = e.attrs.value;
    var list = $('#tokenfield_recipient').tokenfield('getTokensList').split(', ');
    inData = $.inArray(value, data);
    inList = $.inArray(value, list);
    if (inData<0 || inList>=0) {
      return false;
    }
  })
}
$(document).ready(function () {
    $("input[disabled]").siblings('.input-group-addon').off('click');
});

function time_differ(start, finish) {
  if( window.StopDifference != true) {
    var ps = moment($(start).val(), $(start).data('format'));
    var pf = moment($(finish).val(), $(finish).data('format'));
    var diff = pf.diff(ps, 'milliseconds');
    $(finish+'_picker').on('change', $(finish), function () {
      ps = moment($(start).val(), $(start).data('format'));
      pf = moment($(finish).val(), $(finish).data('format'));
    });
      $(start+'_picker').on('change', $(start), function () {
        var start_date = moment($(start).val(), $(start).data('format'));
        var new_finish_date = start_date.add(diff);
        // Updates the finish time box with the appropriate time
        $(finish).val(new_finish_date.format($(finish).data('format')));
        // Updates the finish time DateTimePicker with the appropriate time
        $(finish+'_picker').data('DateTimePicker').setValue(new_finish_date);
      });
      return diff;
  }
}