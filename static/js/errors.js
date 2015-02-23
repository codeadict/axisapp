var image = $('#background-image');

function resize(){
  var width = $(window).width();
  // make room for the error message
  var margin_top = 80;
  if (width < 400){
    margin_top = 120;
  }
  var height = $(window).height() - margin_top;
  if (width / 1052 * 744 < height){
    image.attr('width', width);
    image.attr('height', 'auto');
    // put the image at the bottom of the page
    image.css('position', 'absolute');
    image.css('bottom', 0);
    image.css('left', 0);
  } else {
    image.attr('height', height);
    image.attr('width', 'auto');
    image.css('position', 'static');
    image.css('bottom', 'auto');
    image.css('left', 'auto');
  }
  image.css('margin-top', margin_top + 'px');
}

(function($) {
  var image_id = Math.round(Math.random() * 5.99 + 0.5);
  var url = image.attr('data-path-base');
  var fname = url.match(/d\d*[\.\w]*?\.svg/i)[0];
  url = url.replace(fname, 'd' + image_id + '.svg');
  image.attr('src', url);
  image.show();
  resize();
  $(window).resize(resize);
})(jQuery);

