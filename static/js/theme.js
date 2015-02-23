$panel = $('.panel');
$panel.on('hide.bs.collapse', function (event) {
  if ($(event.target).parent()[0] == this)
    $(this).removeClass('inside');
});

$panel.on('show.bs.collapse', function (event) {
  if ($(event.target).parent()[0] == this)
    $(this).addClass('inside');
});

$('#version').popover();

$('.confirm-follow').click(function(e) {
  var link = $(this).attr('href');
  var method = $(this).data('method');
  e.preventDefault();
  var msg = $(this).attr('msg') || 'Are you sure you wish to continue?';
  bootbox.confirm(msg, function(result) {
    if (result) {
      if (method.toLowerCase() == 'post'){
        var form = $('#button-form');
        form.attr('action', link);
        form.submit();
      }
      else{
        document.location.href = link;
      }
    }
  });
});

// TODO: this could probably be cleaned up to only use data-method
$('.submit-post,[data-method="POST"]').not('.confirm-follow').click(function(e) {
  var link = $(this).attr('href');
  e.preventDefault();
  var form = $('#button-form');
  form.attr('action', link);
  $.each($(this).data(), function(k, v){
    if (k == 'method'){
      return;
    }
    $('<input>').attr({
      type: 'hidden',
      name: k,
      value: v
    }).appendTo(form);
  });
  form.submit();
});

$('.show-box').click(function(e) {
  e.preventDefault();
  bootbox.dialog({
    message: $(this).attr('msg-body'),
    title: $(this).attr('msg-title')
  });
});

function set_active_item(target){
  if (target === '')
    return;
  $('.menu-item.basic').removeClass('active');
  $('[target="' + target + '"]').addClass('active');
}

$(function () {
  function modal_form_submit(form, modal) {
    $(form).submit(function (e) {
      e.preventDefault();
      e.stopPropagation();
      $.ajax({
        type: $(this).attr('method'),
        url: $(this).attr('action'),
        data: $(this).serialize(),
        success: function (xhr, ajaxOptions, thrownError) {
          if ($(xhr).find('.has-error').length > 0 || $(xhr).find('.alert-danger').length > 0) {
            $(modal).find('.modal-body').html(xhr);
            modal_form_submit(form, modal);
          } else {
            $(modal).modal('toggle');
            location.reload();
          }
        },
        error: function (xhr, ajaxOptions, thrownError) {
        }
      });
    });
  }

  $('[data-toggle="crud-modal"]').on('click', function (e) {
        e.preventDefault();
        var url = $(this).attr('href');
        //We get the modal title from link title attribute or from data-title one
        var title = $(this).attr('title') || $(this).data('title');
        if (!url.indexOf('#') == 0) {
            //define the modal structure
            var dialog =  $("<div class='modal fade' tabindex='-1' role='dialog' id='tc-modal'>" +
                        "<div class='modal-dialog'>" +
                          "<div class='modal-content'>" +
                            "<div class='modal-body' id='tc-modal-body'></div>" +
                          "</div>" +
                        "</div>" +
                      "</div>");

            var header = "<div class='modal-header'>" +
                             "<button type='button' class='close' data-dismiss='modal'>" +
                                "<span aria-hidden='true'>&times;</span><span class='sr-only'>Close</span>" +
                             "</button>" +
                             "<h4 class='modal-title'></h4>" +
                         "</div>";

            //here will be loaded the form
            var body = dialog.find(".modal-body");

            //Append the header to modal
            body.before(header);
            //Set the title
            dialog.find(".modal-title").html(title);

            dialog.modal({keyboard: false, backdrop: 'static', show: false})
                .on('hidden.bs.modal', function (e) {
                    if (e.target === this) {
                        dialog.remove();
                    }
                })
                .appendTo('body');

            //get the data from url and render on modal
            $.get(url, function (data) {
                body.html(data);
                $('#tc-modal-body form').attr('action', url);
                dialog.modal('show');
                modal_form_submit('#tc-modal-body form', '#tc-modal');
            });
        }
    });
});

$(document).ready(function(){
  // set the active menu item if item with
  // id enable-hash-menu is defined
  if ($('#enable-hash-menu').length > 0){
    $('.menu-target').click(function() {
      set_active_item($(this).attr('href'));
    });
    $('.menu-item').click(function() {
      set_active_item($(this).attr('target'));
    });
    set_active_item(location.hash);
  }
  // enable tool tips of they exist
  if ($('[data-toggle="tooltip"]').length > 0){
    $('[data-toggle="tooltip"]').tooltip();
  }
});

$(function () {
  $('.ajax-popover').popover({
    html: true,
    placement: 'top',
    title: function () {
      return $(this).text();
    },
    content: function () {
      return set_popover_content($(this).data('content-url'), $(this));
    }
  }).on('click', function(e) {e.preventDefault(); return true;});


  function set_popover_content(url, el){
    $.ajax({
      url: url,
      success: function(response){
        el.data('bs.popover').options.content = response;
        el.popover('show');
      },
      error: function(){
        el.data('bs.popover').options.content = 'Error Occurred';
        el.popover('show');
      }
    });
    return '<div>Loading...</div>';
  }
});